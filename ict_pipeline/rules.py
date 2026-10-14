"""Deterministic hard-rule engine (SPEC section 3). Money decisions live here, never in prompts."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from . import money
from .candles import Bar, is_forming, normal_wick
from .config import INSTRUMENT_SPECS, Settings
from .killzones import active_kill_zones
from .news import NewsCalendar
from .schemas import Blocked, Candidate

# reason codes
RR_BELOW_2 = "RR_BELOW_2"
STOP_TOO_TIGHT = "STOP_TOO_TIGHT"
RISK_UNIT_FULL = "RISK_UNIT_FULL"
OPPOSITE_OPEN = "OPPOSITE_OPEN"
NEWS_BLACKOUT = "NEWS_BLACKOUT"
FORMING_CANDLE = "FORMING_CANDLE"
OUTSIDE_KILL_ZONE = "OUTSIDE_KILL_ZONE"
DUPLICATE = "DUPLICATE"
GUARDRAIL_BLOCKED = "GUARDRAIL_BLOCKED"
NO_EQUITY = "NO_EQUITY_CONFIGURED"

ACTIVE = ("pending", "filled")


@dataclass
class Decision:
    candidate: Candidate
    passed: bool
    reason: Optional[str] = None
    detail: str = ""
    stop: float = 0.0           # padded stop
    rr: float = 0.0
    risk_unit: str = ""
    risk_pct: float = 0.0
    size: Optional[float] = None
    counter_trend: bool = False
    notes: List[str] = field(default_factory=list)
    update_of: Optional[str] = None

    def blocked(self) -> Blocked:
        return Blocked(candidate_id=self.candidate.candidate_id, reason=self.reason or "", detail=self.detail[:300])


class RuleEngine:
    def __init__(self, settings: Settings, calendar: NewsCalendar):
        self.s = settings
        self.cal = calendar

    # rule 3 helper
    def risk_unit(self, instrument: str, direction: str) -> str:
        return self.s.risk_groups.get(f"{instrument}:{direction}", f"{instrument}")

    # rule 5
    def padded_stop(self, c: Candidate, bars_1m: List[Bar]) -> Tuple[float, float, float]:
        spread = float(self.s.spreads.get(c.instrument, INSTRUMENT_SPECS[c.instrument]["spread"]))
        wick = normal_wick(bars_1m, c.direction, self.s.wick_lookback)
        pad = money.D(spread) + money.D(wick)
        if c.direction == "long":
            need = money.D(c.raid_extreme) - pad
            stop = min(money.D(c.stop), need)
        else:
            need = money.D(c.raid_extreme) + pad
            stop = max(money.D(c.stop), need)
        return float(stop), spread, wick

    # Dedupe zone: same instrument + direction with entries within a quarter of the risk distance.

    def evaluate(self, cands: List[Candidate], now: datetime, bars_1m: Dict[str, List[Bar]],
                 open_trades: List[dict], bias: Dict[str, str], htf_dir: Dict[str, str],
                 scores: Dict[str, float] | None = None) -> List[Decision]:
        """Evaluate all candidates of a cycle. ``open_trades`` = trade-state rows (pending/filled)."""
        scores = scores or {}
        active = [t for t in open_trades if t.get("status") in ACTIVE]
        in_kz = bool(active_kill_zones(now))
        decisions: List[Decision] = []
        accepted: List[Decision] = []
        # best first so dedupe keeps the strongest candidate
        order = sorted(cands, key=lambda c: (-scores.get(c.candidate_id, 0), -c.rr_tp1))
        for c in order:
            d = Decision(candidate=c, passed=False)
            decisions.append(d)
            # rule 6: counter-trend recomputed from Bias / HTF (label, never drop)
            b = bias.get(c.instrument, "neutral")
            h = htf_dir.get(c.instrument, "range")
            against = (c.direction == "long" and (b == "bearish" or h == "bear")) or \
                      (c.direction == "short" and (b == "bullish" or h == "bull"))
            d.counter_trend = bool(c.counter_trend or against)
            # rule 8 closed candles
            try:
                sig = datetime.fromisoformat(c.mss_time)
            except ValueError:
                sig = now
            if is_forming(sig, c.tf if c.tf in ("1m", "5m", "15m", "1H", "4H", "D") else "1m", now):
                d.reason, d.detail = FORMING_CANDLE, f"signal bar {c.mss_time} {c.tf} not closed at {now.isoformat()}"
                continue
            # rule 9 kill zones
            if not in_kz:
                d.reason, d.detail = OUTSIDE_KILL_ZONE, now.isoformat()
                continue
            # rule 7 news
            ev = self.cal.blocking_event(c.instrument, now, scalp=(c.agent == "scalp"))
            if ev:
                d.reason, d.detail = NEWS_BLACKOUT, f"{ev.name} {ev.at.isoformat()}"
                continue
            # rule 4 opposite
            opp = [t for t in active + [a.__dict__ | {"instrument": a.candidate.instrument, "direction": a.candidate.direction,
                                                     "trade_id": a.candidate.candidate_id} for a in accepted]
                   if t["instrument"] == c.instrument and t["direction"] != c.direction]
            if opp:
                d.reason, d.detail = OPPOSITE_OPEN, f"{opp[0].get('trade_id')} {opp[0]['direction']} is pending/open"
                continue
            # rule 5 padding, then rule 1 R:R
            stop, spread, wick = self.padded_stop(c, bars_1m.get(c.instrument, []))
            d.stop = stop
            rr_val = money.rr(c.entry, stop, c.tp1, c.direction)
            d.rr = money.q(rr_val, 2)
            moved = stop != c.stop
            if rr_val < money.D(self.s.min_rr):
                d.reason = STOP_TOO_TIGHT if moved else RR_BELOW_2
                d.detail = (f"stop {c.stop} -> {stop} (spread {spread} + wick {money.q(wick, 5)}); R:R {d.rr}" if moved
                            else f"R:R {d.rr} < {self.s.min_rr}")
                continue
            if moved:
                d.notes.append(f"stop padded {c.stop} -> {money.q(stop, 5)}")
            # rule 10 dedupe / updates of existing trade ids
            risk = abs(c.entry - stop)
            existing = [t for t in active if t["instrument"] == c.instrument and t["direction"] == c.direction
                        and abs(float(t["entry"]) - c.entry) <= risk * 0.25]
            if c.trade_id or existing:
                d.update_of = c.trade_id or existing[0]["trade_id"]
                d.reason, d.detail = DUPLICATE, f"update of existing {d.update_of}"
                continue
            same = [a for a in accepted if a.candidate.instrument == c.instrument and a.candidate.direction == c.direction
                    and abs(a.candidate.entry - c.entry) <= max(risk, abs(a.candidate.entry - a.stop)) * 0.25]
            if same:
                d.reason, d.detail = DUPLICATE, f"same entry zone as {same[0].candidate.candidate_id}"
                continue
            # rule 3 shared risk unit + rule 2 sizing
            unit = self.risk_unit(c.instrument, c.direction)
            used = sum(float(t.get("risk_pct", self.s.risk_pct)) for t in active if t.get("risk_unit") == unit)
            used += sum(a.risk_pct for a in accepted if a.risk_unit == unit)
            remaining = money.q(money.D(self.s.risk_pct) - money.D(used), 4)
            d.risk_unit = unit
            if remaining <= 0:
                if self.s.shared_unit_mode == "block":
                    d.reason, d.detail = RISK_UNIT_FULL, f"unit {unit} already uses {used}%"
                    continue
                d.risk_pct = 0.0
                d.notes.append(f"shares unit {unit}: 0% extra while unit is full; full {self.s.risk_pct}% once it closes")
            else:
                d.risk_pct = remaining
                if used:
                    d.notes.append(f"shares unit {unit}: {remaining}% of {self.s.risk_pct}%")
            spec = INSTRUMENT_SPECS[c.instrument]
            d.size = money.position_size(self.s.equity, d.risk_pct, c.entry, stop, spec["value_per_point"])
            if self.s.equity is None:
                d.notes.append("size: set EQUITY to compute lots (equity x risk% / (stop dist x value/pt))")
            d.passed = True
            accepted.append(d)
        return decisions
