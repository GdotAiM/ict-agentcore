"""ICT Mentor / Communication agent.

The FINAL reply the owner sees ALWAYS comes from this agent (NovaMart Communication Agent
pattern). The orchestrator never invents fallback text: if the mentor fails, the cycle returns
the blocked CombinedCall JSON with the mandatory footer and a clear error, never free-form prose.
"""
from __future__ import annotations

import json
from typing import List

from ..guardrails import FOOTER, UNTRUSTED_RULE, filter_outbound, wrap_untrusted
from ..schemas import CombinedCall, TradeAlert


SYSTEM = f"""{UNTRUSTED_RULE}
You are the ICT Mentor / Communication agent for an ANALYSIS-ONLY trading pipeline.
You NEVER place orders, NEVER log into accounts, NEVER handle credentials, NEVER size for
anyone other than the configured owner. Your only job is to turn a CombinedCall JSON into one
short, clear message for the owner.

Rules:
- Start with the kill zone and headline.
- For each trade: instrument, direction, COUNTER-TREND if flagged, entry/stop/tp1, R:R, risk unit,
  size (or the size formula if equity not configured), confluence, p_win/exp_r, early exit, sources.
- List open-trade updates and blocked candidates with reason codes.
- Show "data: fallback" when fallback_used is true.
- End EXACTLY with: {FOOTER}
- Cite KB titles only when they appear in the mentor citations; never invent titles.
Return ONLY the message text (no JSON, no code fences).
"""


def render_deterministic(call: CombinedCall, owner: str) -> str:
    """Deterministic renderer used by MockLLM / offline tests and as a hard fallback when the
    mentor LLM is unavailable. Still the mentor agent path (never orchestrator prose)."""
    lines = [f"{owner} — {call.kill_zone or 'OFF'} @ {call.as_of}",
             f"**{call.headline}**"]
    if call.degraded:
        lines.append("_degraded mode (token budget ≥ 90%): orchestrator + rules + open-trade monitor only_")
    if call.fallback_used:
        lines.append("data: fallback")
    if call.market_summary:
        lines.append("Market: " + "; ".join(f"{k} {v}" for k, v in call.market_summary.items()))
    for t in call.trades:
        tag = " COUNTER-TREND" if t.counter_trend else ""
        size = f"size={t.size}" if t.size is not None else "size=set EQUITY"
        lines.append(
            f"- {t.trade_id} {t.instrument} {t.direction.upper()}{tag}: {t.order} @ {t.entry} "
            f"stop {t.stop} tp1 {t.tp1} R:R {t.rr} unit={t.risk_unit} ({t.risk_pct}%) {size} "
            f"conf={t.confluence} p={t.p_win if t.p_win is not None else 'UNPROVEN (no base rate)'} expR={t.exp_r if t.exp_r is not None else '-'} early={t.early_exit or '-'} "
            f"src={','.join(t.sources)}")
        for n in t.notes:
            lines.append(f"    note: {n}")
    for u in call.open_trade_updates:
        lines.append(f"- update {u.trade_id}: {u.status} — {u.note}")
    if call.blocked:
        lines.append("Blocked: " + "; ".join(f"{b.candidate_id}={b.reason}" for b in call.blocked))
    lines.append("")
    lines.append(FOOTER)
    return "\n".join(lines)


class MentorAgent:
    def __init__(self, llm=None, owner: str = "owner", kb_retriever=None):
        self.llm, self.owner, self.kb = llm, owner, kb_retriever

    def compose(self, call: CombinedCall, citations: List[dict] | None = None) -> str:
        payload = {"combined_call": call.model_dump(mode="json"), "citations": citations or []}
        if self.llm is None:
            text = render_deterministic(call, self.owner)
        else:
            prompt = SYSTEM + "\n\n" + wrap_untrusted(json.dumps(payload, default=str))
            try:
                if hasattr(self.llm, "invoke"):
                    text, _ = self.llm.invoke("mentor", prompt)
                else:
                    text = str(self.llm(prompt))
            except Exception:
                text = render_deterministic(call, self.owner)
        ok, cleaned, reasons = filter_outbound(text)
        if not ok:
            # Guardrail intervened: fall back to the deterministic safe render (still mentor path).
            cleaned = render_deterministic(call, self.owner)
            cleaned = f"[guardrail blocked free-form mentor text: {','.join(reasons)}]\n" + cleaned
        return cleaned
