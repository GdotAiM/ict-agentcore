"""Shared agent helpers: envelope validation, as_of/staleness rejection, mocked LLM for offline tests."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional

from pydantic import ValidationError

from ..guardrails import UNTRUSTED_RULE, wrap_untrusted
from ..observability import RunLog
from ..schemas import Envelope, FinderOutput


@dataclass
class AgentResult:
    agent: str
    ok: bool
    data: Optional[dict]
    error: str = ""
    latency_ms: float = 0.0
    tokens: int = 0


class MockLLM:
    """Deterministic offline LLM. ``responses`` maps agent-name -> JSON-able dict / callable."""

    def __init__(self, responses: Dict[str, Any] | None = None, tokens: int = 100):
        self.responses = responses or {}
        self.tokens = tokens
        self.calls = []

    def invoke(self, agent: str, prompt: str) -> tuple[str, int]:
        self.calls.append((agent, prompt[:200]))
        r = self.responses.get(agent)
        if callable(r):
            r = r(prompt)
        if r is None:
            raise RuntimeError(f"MockLLM has no response for {agent}")
        return (r if isinstance(r, str) else json.dumps(r)), self.tokens


def validate_envelope(raw: dict, expected_agent: str) -> dict:
    env = Envelope.model_validate(raw)
    if env.agent != expected_agent:
        raise ValidationError.from_exception_data("Envelope", [{"type": "value_error", "loc": ("agent",),
                                                                "input": env.agent, "ctx": {"error": f"expected {expected_agent}"}}])
    return env.model_dump(mode="json")


def validate_finder(raw: dict, expected_agent: str) -> dict:
    out = FinderOutput.model_validate(raw)
    if out.agent != expected_agent:
        raise ValueError(f"expected agent {expected_agent}, got {out.agent}")
    return out.model_dump(mode="json")


def check_staleness(as_of: datetime, cycle_as_of: datetime, max_skew: timedelta = timedelta(minutes=0)) -> bool:
    """True if the agent output is stale vs the current cycle snapshot (SPEC: reject older than cycle)."""
    return as_of < cycle_as_of - max_skew


_CLIP = {"notes": 300, "reason": 200, "invalidation_note": 200}


def _clip_text_fields(obj):
    """LLMs overrun free-text length caps; clip those (only) instead of discarding the whole read.
    Prices/levels are never touched, so validation still rejects anything structurally wrong."""
    if isinstance(obj, dict):
        return {k: (v[:_CLIP[k] - 1] + "…" if k in _CLIP and isinstance(v, str) and len(v) > _CLIP[k]
                    else _clip_text_fields(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clip_text_fields(x) for x in obj]
    return obj


class AgentRunner:
    """Wraps an LLM (Strands Agent or MockLLM) so the orchestrator always gets AgentResult."""

    def __init__(self, name: str, llm, validator: Callable, run_log: Optional[RunLog] = None, system: str = ""):
        self.name, self.llm, self.validator, self.run_log = name, llm, validator, run_log
        self.system = system or UNTRUSTED_RULE

    def run(self, prompt_obj: dict, cycle_as_of: datetime) -> AgentResult:
        t0 = time.time()
        prompt = self.system + "\n\n" + wrap_untrusted(json.dumps(prompt_obj, default=str))
        try:
            if hasattr(self.llm, "invoke"):
                text, tokens = self.llm.invoke(self.name, prompt)
            else:  # Strands Agent
                result = self.llm(prompt)
                text = str(result)
                tokens = int(getattr(getattr(result, "metrics", None), "input_tokens", 0) or 0) + \
                         int(getattr(getattr(result, "metrics", None), "output_tokens", 0) or 0)
            # agents must return JSON only
            start = text.find("{"); end = text.rfind("}")
            raw = json.loads(text[start:end + 1] if start >= 0 else text)
            data = self.validator(_clip_text_fields(raw))
            as_of = datetime.fromisoformat(data["as_of"]) if isinstance(data["as_of"], str) else data["as_of"]
            if check_staleness(as_of, cycle_as_of):
                raise ValueError(f"stale as_of={as_of.isoformat()} cycle={cycle_as_of.isoformat()}")
            res = AgentResult(self.name, True, data, latency_ms=(time.time() - t0) * 1000, tokens=tokens)
        except Exception as e:
            res = AgentResult(self.name, False, None, error=f"{type(e).__name__}: {e}",
                              latency_ms=(time.time() - t0) * 1000)
        if not res.ok:
            import logging
            logging.getLogger("ict.agents").warning("agent %s invalid output: %s", self.name, res.error[:500])
        if self.run_log:
            self.run_log.agent_call(self.name, prompt_obj, res.data, res.latency_ms, res.tokens, res.ok, res.error)
        return res
