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
    attempts: int = 1          # 1 = first answer was valid; 2+ = validate-and-repair loop ran
    repaired: bool = False     # True when a repair attempt turned an invalid answer into a valid one


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


class StaleOutputError(ValueError):
    """Agent output is older than the cycle snapshot. Never repaired: asking the model to "fix" a
    timestamp would just invite it to invent a fresh one."""


def _summarise_errors(e: Exception, limit: int = 6) -> str:
    """Compact, model-readable list of what failed (field path + message), capped in length."""
    if isinstance(e, ValidationError):
        lines = [f"- {'.'.join(str(x) for x in err.get('loc', ())) or '<root>'}: {err.get('msg', '')}"
                 for err in e.errors()[:limit]]
        if len(e.errors()) > limit:
            lines.append(f"- … {len(e.errors()) - limit} more")
        return "\n".join(lines)
    if isinstance(e, json.JSONDecodeError):
        return f"- output was not valid JSON ({e.msg} at char {e.pos})"
    return f"- {type(e).__name__}: {str(e)[:300]}"


REPAIR_INSTRUCTION = (
    "Your previous answer failed schema validation and was NOT used.\n"
    "Validation errors:\n{errors}\n"
    "Return the corrected answer as ONE JSON object only, same schema, no prose. "
    "Fix only the fields listed; keep as_of and every price/level grounded in the snapshot above."
)


class AgentRunner:
    """Wraps an LLM (Strands Agent or MockLLM) so the orchestrator always gets AgentResult.

    Validate-and-repair (self-correction) loop: if the JSON fails to parse or fails pydantic
    validation, the runner re-prompts the same agent once (``max_repairs``) with the exact
    validation errors. Stale ``as_of`` is never repaired. If the repair also fails, the result is
    ``ok=False`` and the orchestrator discards it exactly as before (SPEC §2, acceptance test 2).
    Code still owns the decision: a repaired output goes through the same validator and the
    hard-rule engine downstream.
    """

    def __init__(self, name: str, llm, validator: Callable, run_log: Optional[RunLog] = None, system: str = "",
                 max_repairs: int = 1):
        self.name, self.llm, self.validator, self.run_log = name, llm, validator, run_log
        self.system = system or UNTRUSTED_RULE
        self.max_repairs = max(0, int(max_repairs))

    def _call(self, prompt: str) -> tuple[str, int]:
        if hasattr(self.llm, "invoke"):
            return self.llm.invoke(self.name, prompt)
        result = self.llm(prompt)  # Strands Agent
        tokens = int(getattr(getattr(result, "metrics", None), "input_tokens", 0) or 0) + \
                 int(getattr(getattr(result, "metrics", None), "output_tokens", 0) or 0)
        return str(result), tokens

    def _parse_and_validate(self, text: str, cycle_as_of: datetime) -> dict:
        # agents must return JSON only
        start = text.find("{"); end = text.rfind("}")
        raw = json.loads(text[start:end + 1] if start >= 0 else text)
        data = self.validator(_clip_text_fields(raw))
        as_of = datetime.fromisoformat(data["as_of"]) if isinstance(data["as_of"], str) else data["as_of"]
        if check_staleness(as_of, cycle_as_of):
            raise StaleOutputError(f"stale as_of={as_of.isoformat()} cycle={cycle_as_of.isoformat()}")
        return data

    def run(self, prompt_obj: dict, cycle_as_of: datetime) -> AgentResult:
        t0 = time.time()
        prompt = self.system + "\n\n" + wrap_untrusted(json.dumps(prompt_obj, default=str))
        tokens_total, attempts, data, err = 0, 0, None, None
        current = prompt
        while True:
            attempts += 1
            try:
                text, tokens = self._call(current)
                tokens_total += int(tokens or 0)
                data = self._parse_and_validate(text, cycle_as_of)
                err = None
                break
            except (json.JSONDecodeError, ValidationError, ValueError, KeyError, TypeError) as e:
                err = e
                if isinstance(e, StaleOutputError) or attempts > self.max_repairs:
                    break
                current = prompt + "\n\n" + REPAIR_INSTRUCTION.format(errors=_summarise_errors(e))
            except Exception as e:  # transport / model errors are not schema problems: no repair
                err = e
                break
        latency = (time.time() - t0) * 1000
        if err is None:
            res = AgentResult(self.name, True, data, latency_ms=latency, tokens=tokens_total,
                              attempts=attempts, repaired=attempts > 1)
        else:
            res = AgentResult(self.name, False, None, error=f"{type(err).__name__}: {err}",
                              latency_ms=latency, tokens=tokens_total, attempts=attempts)
        if not res.ok:
            import logging
            logging.getLogger("ict.agents").warning("agent %s invalid output after %d attempt(s): %s",
                                                    self.name, attempts, res.error[:500])
        if self.run_log:
            self.run_log.agent_call(self.name, prompt_obj, res.data, res.latency_ms, res.tokens, res.ok, res.error,
                                    attempts=res.attempts, repaired=res.repaired)
        return res
