"""News blackout (rule 7): no new fills from T-15m, flat/cancel at T-5m, scalps also avoid T+15m."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from zoneinfo import ZoneInfo

RELEVANT = {"NAS100": {"USD"}, "XAUUSD": {"USD"}, "EURUSD": {"USD", "EUR"}, "GBPUSD": {"USD", "GBP"}, "DXY": {"USD"}}


@dataclass(frozen=True)
class NewsEvent:
    name: str
    currency: str
    at: datetime  # aware
    impact: str = "high"


def load_calendar(path: str) -> List[NewsEvent]:
    try:
        with open(path) as f:
            raw = json.load(f)
    except FileNotFoundError:
        return []
    out = []
    for e in raw.get("events", []):
        tz = ZoneInfo(e.get("tz", "America/New_York"))
        at = datetime.fromisoformat(f"{e['date']}T{e['time']}").replace(tzinfo=tz)
        out.append(NewsEvent(e["name"], e["currency"], at, e.get("impact", "high")))
    return out


class NewsCalendar:
    def __init__(self, events: List[NewsEvent], pre_block_min=15, flat_min=5, scalp_post_min=15):
        self.events = [e for e in events if e.impact == "high"]
        self.pre = timedelta(minutes=pre_block_min)
        self.flat = timedelta(minutes=flat_min)
        self.post = timedelta(minutes=scalp_post_min)

    def _relevant(self, instrument: str):
        cur = RELEVANT.get(instrument, {"USD"})
        return [e for e in self.events if e.currency in cur]

    def blocking_event(self, instrument: str, t: datetime, scalp: bool = False) -> Optional[NewsEvent]:
        """Event that forbids a NEW fill / alert at ``t``. Window = [T-15m, T] (+15m after for scalps).

        Non-scalp entries are also held until the release bar has closed (T+1m)."""
        for e in self._relevant(instrument):
            end = e.at + (self.post if scalp else timedelta(minutes=1))
            if e.at - self.pre <= t < end:
                return e
        return None

    def must_be_flat(self, instrument: str, t: datetime) -> Optional[NewsEvent]:
        """Event for which open/pending trades must be closed/cancelled at ``t`` (from T-5m to T+1m)."""
        for e in self._relevant(instrument):
            if e.at - self.flat <= t < e.at + timedelta(minutes=1):
                return e
        return None

    def flat_time(self, e: NewsEvent) -> datetime:
        return e.at - self.flat

    def no_fill_from(self, e: NewsEvent) -> datetime:
        return e.at - self.pre
