"""Candle helpers: closed-bar filtering (rule 8), normal wick (rule 5), resampling."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from statistics import median
from typing import Iterable, List

TF_MINUTES = {"1m": 1, "5m": 5, "15m": 15, "1H": 60, "4H": 240, "D": 1440}


@dataclass(frozen=True)
class Bar:
    time: datetime  # bar OPEN time, aware
    open: float
    high: float
    low: float
    close: float
    tf: str = "1m"

    @property
    def close_time(self) -> datetime:
        return self.time + timedelta(minutes=TF_MINUTES[self.tf])

    def is_closed(self, now: datetime) -> bool:
        return self.close_time <= now


def closed_only(bars: Iterable[Bar], now: datetime) -> List[Bar]:
    return [b for b in bars if b.is_closed(now)]


def is_forming(signal_bar_open: datetime, tf: str, now: datetime) -> bool:
    return signal_bar_open + timedelta(minutes=TF_MINUTES.get(tf, 1)) > now


def normal_wick(bars: List[Bar], direction: str, n: int = 60) -> float:
    """Median 1m wick on the stop side over the last ``n`` closed candles.

    long -> lower wick (min(open,close) - low); short -> upper wick (high - max(open,close)).
    """
    recent = bars[-n:]
    if not recent:
        return 0.0
    if direction == "long":
        w = [min(b.open, b.close) - b.low for b in recent]
    else:
        w = [b.high - max(b.open, b.close) for b in recent]
    return float(median(w))


def resample(bars: List[Bar], tf: str) -> List[Bar]:
    mins = TF_MINUTES[tf]
    out: dict = {}
    for b in bars:
        t = b.time
        floored = t - timedelta(minutes=(t.hour * 60 + t.minute) % mins, seconds=t.second, microseconds=t.microsecond)
        cur = out.get(floored)
        if cur is None:
            out[floored] = [b.open, b.high, b.low, b.close]
        else:
            cur[1] = max(cur[1], b.high); cur[2] = min(cur[2], b.low); cur[3] = b.close
    return [Bar(t, *v, tf=tf) for t, v in sorted(out.items())]
