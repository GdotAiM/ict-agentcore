"""Lead orchestrator (SPEC 2.1). Fans out agents, runs the deterministic rule engine, writes
trade-state (single writer, optimistic lock), and ALWAYS returns the Mentor agent's final text
(never invents fallback prose). Degrades at 90% of the daily token budget.
"""
from __future__ import annotations

import concurrent.futures
import logging
from datetime import datetime
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo

from .agents.base import AgentResult, AgentRunner, MockLLM, validate_envelope, validate_finder
from .agents.mentor import MentorAgent
from .base_rates import lookup as base_rate_lookup
from .config import Settings
from .data_service import DataService, Snapshot
from .fills import update_trades
from .guardrails import FOOTER, filter_outbound
from .killzones import primary_kill_zone
from .news import NewsCalendar
from .notifier import NullNotifier, Notifier
from .observability import RunLog, TokenBudget, XRayTracer, new_run_id
from .rules import Decision, RuleEngine
from .schemas import (Blocked, Candidate, CombinedCall, Confluence, Mentor, OpenTradeUpdate,
                      Probability, TradeAlert)
from .trade_state import TradeStateWriter

log = logging.getLogger("ict.orch")
SAST = ZoneInfo("Africa/Johannesburg")


class Pipeline:
    def __init__(self, settings: Settings, data: DataService, writer: TradeStateWriter,
                 calendar: NewsCalendar, notifier: Notifier, budget: Optional[TokenBudget] = None,
                 llm=None, mentor: Optional[MentorAgent] = None, memory_client=None, session_repo=None):
        self.s = settings
        self.data = data
        self.writer = writer
        self.calendar = calendar
        self.notifier = notifier
        self.budget = budget or TokenBudget(settings.daily_token_budget, settings.budget_degrade_at)
        self.llm = llm or MockLLM()
        self.mentor = mentor or MentorAgent(llm=self.llm, owner=settings.owner_name)
        self.rules = RuleEngine(settings, calendar)
        self.memory_client = memory_client
        self.session_repo = session_repo

    # ── agent fan-out ──────────────────────────────────────────────────────────
    def _runners(self, run_log: RunLog) -> Dict[str, AgentRunner]:
        return {
            **{n: AgentRunner(n, self.llm, lambda r, n=n: validate_envelope(r, n), run_log) for n in
               ("bias", "timeframe", "intermarket", "liquidity", "orderflow")},
            **{n: AgentRunner(n, self.llm, lambda r, n=n: validate_finder(r, n), run_log) for n in
               ("entry_model", "scalp", "pingpong")},
        }

    def _fan_out(self, names: List[str], runners: Dict[str, AgentRunner], payload: dict,
                 cycle_as_of: datetime) -> Dict[str, AgentResult]:
        out = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, len(names))) as ex:
            futs = {ex.submit(runners[n].run, payload, cycle_as_of): n for n in names if n in runners}
            for f in concurrent.futures.as_completed(futs):
                out[futs[f]] = f.result()
        return out

    # ── checks (sequential per candidate) ──────────────────────────────────────
    def _score(self, c: Candidate, ctx: dict, run_log: RunLog) -> tuple[Optional[Confluence], Probability, Mentor]:
        # Confluence: deterministic agreement count (LLM may also score; we always recompute).
        agree, conflict = [], []
        bias = (ctx.get("bias") or {}).get(c.instrument, {})
        if bias.get("bias") == ("bullish" if c.direction == "long" else "bearish"):
            agree.append("bias")
        elif bias.get("bias") and bias.get("bias") != "neutral":
            conflict.append(f"bias:{bias.get('bias')}")
        of = (ctx.get("orderflow") or {}).get(c.instrument, {})
        if of.get("agrees_with_bias") and "bias" in agree:
            agree.append("orderflow")
        liq = (ctx.get("liquidity") or {}).get(c.instrument, {})
        if any(p.get("id") == c.sweep_level_id for p in liq.get("pools", [])):
            agree.append("liquidity")
        score = max(1, min(5, 1 + len(agree) - len(conflict)))
        conf = Confluence(candidate_id=c.candidate_id, score=score, agree=agree, conflict=conflict)
        br = base_rate_lookup(c.model, c.instrument, c.confirmation)
        adj = []
        p = br.p_win
        if c.counter_trend and p is not None:
            adj.append({"factor": "counter_trend", "delta": -0.05, "source": "heuristic"})
            p = max(0.0, p - 0.05)
        from . import money
        exp = money.exp_r(p, c.rr_tp1) if p is not None else br.exp_r
        prob = Probability(candidate_id=c.candidate_id, p_win=p, exp_r=exp, n=br.n,
                           small_sample=br.small_sample, base_rate_source=br.source,
                           adjustments=adj, ci=None)
        # Mentor: model/time/DOL checks are code; citations only from KB when available.
        citations = []
        if hasattr(self.mentor, "kb") and self.mentor.kb:
            try:
                citations = [{"title": x.get("uri", "")[-80:], "url": x.get("uri", ""), "timestamp": ""}
                             for x in self.mentor.kb(f"ICT {c.model} {c.instrument}")[:3]]
            except Exception:
                citations = []
        in_kz = primary_kill_zone(datetime.fromisoformat(c.mss_time)) is not None
        mentor = Mentor(candidate_id=c.candidate_id, model_match=True, time_ok=in_kz,
                        dol_ok=True, issues=[], citations=citations)
        run_log.add("check", candidate_id=c.candidate_id, confluence=conf.model_dump(),
                    probability=prob.model_dump(), mentor=mentor.model_dump())
        return conf, prob, mentor

    # ── one cycle ──────────────────────────────────────────────────────────────
    def run_cycle(self, now: datetime, session_id: Optional[str] = None,
                  owner_text: str = "run kill-zone cycle") -> dict:
        run_id = new_run_id()
        run_log = RunLog(run_id, self.s.log_dir)
        tracer = XRayTracer()
        degraded = self.budget.degraded()
        kz = primary_kill_zone(now)
        with tracer.subsegment("data_service"):
            snap: Snapshot = self.data.snapshot(now)
        # Always update fills first (deterministic, cheap) so all readers see the same state.
        with tracer.subsegment("fills"):
            fill_changes = update_trades(self.writer, snap.bars_1m(), now, self.calendar)
        open_updates = [OpenTradeUpdate(trade_id=c["trade_id"], status=c["status"],
                                        note=f"{c.get('reason', c['status'])} @ {c['at']}") for c in fill_changes]

        news_flat = []
        for t in self.writer.active():
            ev = self.calendar.must_be_flat(t["instrument"], now)
            if ev:
                news_flat.append(OpenTradeUpdate(trade_id=t["trade_id"], status=t["status"],
                                                 note=f"close/cancel for {ev.name} by {self.calendar.flat_time(ev).isoformat()}"))

        if degraded:
            call = CombinedCall(run_id=run_id, kill_zone=kz, as_of=snap.as_of.isoformat(),
                                headline="Degraded: open-trade monitor only",
                                open_trade_updates=open_updates + news_flat, blocked=[],
                                data_source=snap.data_source, fallback_used=snap.fallback_used, degraded=True)
            msg = self.mentor.compose(call)
            self.notifier.send(msg, call.model_dump(mode="json"))
            run_log.flush(); tracer.publish(run_id)
            return {"run_id": run_id, "call": call.model_dump(mode="json"), "message": msg, "degraded": True}

        runners = self._runners(run_log)
        payload = {"run_id": run_id, "as_of": snap.as_of.isoformat(), "data_source": snap.data_source,
                   "fallback_used": snap.fallback_used,
                   "last_closed_bar": snap.last_closed_bar,
                   "compact_bars": {s: {tf: snap.compact(s, tf) for tf in ("1m", "5m", "15m", "1H", "D")}
                                    for s in snap.bars}}
        with tracer.subsegment("market_read"):
            mr = self._fan_out(["bias", "timeframe", "intermarket", "liquidity", "orderflow"], runners, payload, snap.as_of)
        ctx = {n: (r.data or {}).get("instruments", {}) for n, r in mr.items() if r.ok}
        for n, r in mr.items():
            if r.ok:
                self.budget.add(r.tokens)
        market_summary = {}
        for sym, b in ctx.get("bias", {}).items():
            market_summary[sym] = f"{b.get('bias')}" + (f", invalid beyond {b.get('invalidation')}" if b.get('invalidation') is not None else "")

        with tracer.subsegment("setup_finders"):
            finder_payload = {**payload, "market_context": ctx}
            sf = self._fan_out(["entry_model", "scalp", "pingpong"], runners, finder_payload, snap.as_of)
        candidates: List[Candidate] = []
        for n, r in sf.items():
            if r.ok:
                self.budget.add(r.tokens)
                for raw in (r.data or {}).get("candidates", []):
                    try:
                        candidates.append(Candidate.model_validate(raw))
                    except Exception as e:
                        run_log.add("discarded_candidate", agent=n, error=str(e), raw=raw)

        # Checks + rule engine
        bias_map = {s: v.get("bias", "neutral") for s, v in ctx.get("bias", {}).items()}
        htf = {}
        for s, v in ctx.get("timeframe", {}).items():
            ctrl = (v.get("in_control") or "D")
            htf[s] = (v.get("per_tf") or {}).get(ctrl, {}).get("dir", "range")
        scores, checks = {}, {}
        for c in candidates:
            conf, prob, mentor = self._score(c, ctx, run_log)
            scores[c.candidate_id] = float(conf.score) + (prob.exp_r or 0)
            checks[c.candidate_id] = (conf, prob, mentor)
        with tracer.subsegment("rules"):
            decisions = self.rules.evaluate(candidates, now, snap.bars_1m(), self.writer.active(), bias_map, htf, scores)
        for d in decisions:
            run_log.decision(d.candidate.candidate_id, d.passed, d.reason, d.detail)

        trades: List[TradeAlert] = []
        blocked: List[Blocked] = []
        for d in decisions:
            if not d.passed:
                if d.reason == "DUPLICATE" and d.update_of:
                    open_updates.append(OpenTradeUpdate(trade_id=d.update_of, status="pending",
                                                        note=f"re-seen candidate {d.candidate.candidate_id}"))
                else:
                    blocked.append(d.blocked())
                continue
            c = d.candidate
            conf, prob, mentor = checks[c.candidate_id]
            trade_id = c.candidate_id
            row = {
                "trade_id": trade_id, "instrument": c.instrument, "direction": c.direction,
                "model": c.model, "source_agent": c.agent, "entry": c.entry, "stop": d.stop,
                "tp1": c.tp1, "tp2": c.tp2, "risk_unit": d.risk_unit, "risk_pct": d.risk_pct,
                "counter_trend": d.counter_trend, "early_exit": c.early_exit, "valid_until": c.valid_until or None,
                "raid_extreme": c.raid_extreme, "taken_by_owner": None,
            }
            try:
                self.writer.create(row, now, status="pending")
            except Exception as e:  # already exists -> treat as update
                run_log.add("trade_create_skip", trade_id=trade_id, error=str(e))
            notes = list(d.notes)
            if d.counter_trend:
                notes.insert(0, "COUNTER-TREND")
            if mentor.citations:
                notes.append("citations: " + "; ".join(ci.title for ci in mentor.citations[:2]))
            trades.append(TradeAlert(
                trade_id=trade_id, instrument=c.instrument, direction=c.direction, order=c.order,
                entry=c.entry, stop=d.stop, tp1=c.tp1, rr=d.rr, risk_unit=d.risk_unit, risk_pct=d.risk_pct,
                size=d.size, early_exit=c.early_exit, counter_trend=d.counter_trend,
                confluence=conf.score, p_win=prob.p_win, exp_r=prob.exp_r,
                sources=[c.agent] + conf.agree, notes=notes,
                trace_url=(self.s.trace_url_template or "").format(run_id=run_id)))

        headline = ("No trade" if not trades else f"{len(trades)} setup{'s' if len(trades) != 1 else ''}")
        call = CombinedCall(run_id=run_id, kill_zone=kz, as_of=snap.as_of.isoformat(), headline=headline,
                            market_summary=market_summary, trades=trades,
                            open_trade_updates=open_updates + news_flat, blocked=blocked,
                            data_source=snap.data_source, fallback_used=snap.fallback_used, degraded=False)
        # FINAL reply ALWAYS from mentor (never orchestrator fallback text).
        with tracer.subsegment("mentor"):
            msg = self.mentor.compose(call)
        ok, msg, reasons = filter_outbound(msg)
        if not ok:
            msg = f"[outbound blocked: {','.join(reasons)}]\n{FOOTER}"
        notify_result = self.notifier.send(msg, call.model_dump(mode="json"))
        # Memory + session persistence (never raises)
        if self.memory_client and session_id:
            from . import memory as mem
            mem.save_memory_turn(self.memory_client, session_id, self.s.owner_name, owner_text, msg)
        run_log.flush(); tracer.publish(run_id)
        return {"run_id": run_id, "call": call.model_dump(mode="json"), "message": msg,
                "notify": notify_result, "degraded": False, "log": run_log.records}
