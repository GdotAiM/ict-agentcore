"""Fill / exit detection, computed ONCE in code from closed 1m candles (SPEC section 5).

* limit fills when a closed candle trades through entry (long: low <= entry; short: high >= entry)
* stop / TP by first touch; same candle touching both (or fill candle touching stop) = stop first
* early exit "1m close > X" / "1m close < X" on a closed candle
* news: no fills from T-15m (pending order cancelled), flat at T-5m (exit at that bar's open)
* pending past valid_until -> expired
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import List, Optional

from . import money
from .candles import Bar, closed_only
from .news import NewsCalendar
from .trade_state import TradeStateWriter

_EARLY = re.compile(r"1m close\s*([<>])\s*([0-9.]+)")


def _touch_stop(t, b: Bar) -> bool:
    return b.low <= t["stop"] if t["direction"] == "long" else b.high >= t["stop"]


def _touch_tp(t, b: Bar) -> bool:
    return b.high >= t["tp1"] if t["direction"] == "long" else b.low <= t["tp1"]


def _early(t, b: Bar) -> bool:
    m = _EARLY.search(t.get("early_exit") or "")
    if not m:
        return False
    lvl = float(m.group(2))
    return b.close > lvl if m.group(1) == ">" else b.close < lvl


def _ts(b: Bar) -> str:
    return b.time.isoformat()


def update_trades(writer: TradeStateWriter, bars_by_symbol: dict, now: datetime,
                  calendar: Optional[NewsCalendar] = None) -> List[dict]:
    """Advance every pending/filled trade over newly closed 1m bars. Returns list of change notes."""
    changes = []
    for t in writer.active():
        bars = closed_only(bars_by_symbol.get(t["instrument"], []), now)
        last_seen = t.get("last_bar") or t["created_at"]
        last_seen_dt = datetime.fromisoformat(last_seen)
        new = [b for b in bars if b.time >= last_seen_dt and (t.get("last_bar") is None or b.time > last_seen_dt)]
        if t.get("last_bar") is None:  # first evaluation: bars from the creation minute on
            created = datetime.fromisoformat(t["created_at"]).replace(second=0, microsecond=0)
            new = [b for b in bars if b.time >= created]
        status, cur = t["status"], t
        for b in new:
            ev_flat = calendar.must_be_flat(t["instrument"], b.time) if calendar else None
            ev_block = calendar.blocking_event(t["instrument"], b.time) if calendar else None
            if status == "pending":
                vu = t.get("valid_until")
                if vu and b.time >= datetime.fromisoformat(vu):
                    cur = writer.transition_retry(t["trade_id"], "expired", b.time, "valid_until reached", last_bar=_ts(b))
                    status = "expired"; changes.append({"trade_id": t["trade_id"], "status": "expired", "at": _ts(b)}); break
                touched = b.low <= t["entry"] if t["direction"] == "long" else b.high >= t["entry"]
                if ev_block or ev_flat:
                    if touched or ev_flat:
                        cur = writer.transition_retry(t["trade_id"], "cancelled", b.time,
                                                      f"news blackout {(ev_block or ev_flat).name}", last_bar=_ts(b),
                                                      exit_reason="news_flat")
                        status = "cancelled"; changes.append({"trade_id": t["trade_id"], "status": "cancelled", "at": _ts(b)}); break
                    continue
                if touched:
                    stopped_same = _touch_stop(t, b)
                    cur = writer.transition_retry(t["trade_id"], "filled", b.time, "limit traded through",
                                                  fill_time=_ts(b), fill_price=t["entry"], last_bar=_ts(b))
                    status = "filled"; changes.append({"trade_id": t["trade_id"], "status": "filled", "at": _ts(b)})
                    if stopped_same:  # same-candle ambiguity: stop first
                        cur = writer.transition_retry(t["trade_id"], "closed", b.time, "stop (same candle as fill)",
                                                      close_time=_ts(b), exit_price=t["stop"], exit_reason="stop",
                                                      result_r=-1.0, last_bar=_ts(b))
                        status = "closed"; changes.append({"trade_id": t["trade_id"], "status": "closed", "r": -1.0, "at": _ts(b)}); break
                    continue
            elif status == "filled":
                fp = t.get("fill_price", t["entry"])
                exit_px = reason = None
                if ev_flat:
                    exit_px, reason = b.open, "news_flat"
                elif _touch_stop(t, b):          # stop first, even if TP touched in the same candle
                    exit_px, reason = t["stop"], "stop"
                elif _touch_tp(t, b):
                    exit_px, reason = t["tp1"], "tp1"
                elif _early(t, b):
                    exit_px, reason = b.close, "early_exit"
                if exit_px is not None:
                    r = -1.0 if reason == "stop" else money.r_multiple(fp, t["stop"], exit_px, t["direction"])
                    cur = writer.transition_retry(t["trade_id"], "closed", b.time, reason, close_time=_ts(b),
                                                  exit_price=exit_px, exit_reason=reason, result_r=r, last_bar=_ts(b))
                    status = "closed"; changes.append({"trade_id": t["trade_id"], "status": "closed", "r": r,
                                                       "reason": reason, "at": _ts(b)}); break
        if status in ("pending", "filled") and new:
            writer.transition_retry(t["trade_id"], None, now, "monitor", record_history=False, last_bar=_ts(new[-1]))
    return changes
