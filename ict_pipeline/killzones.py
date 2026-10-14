"""Kill-zone clock (rule 9). Defined in New York time and converted with zoneinfo: never hard-code SAST."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import List, Optional
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")
SAST = ZoneInfo("Africa/Johannesburg")

# name -> (start NY, end NY, starts on previous NY day)
KILL_ZONES = {
    "ASIAN": (time(20, 0), time(0, 0), True),
    "LONDON_OPEN": (time(2, 0), time(5, 0), False),
    "NY_AM": (time(7, 0), time(10, 0), False),
    "SILVER_BULLET": (time(10, 0), time(11, 0), False),
    "LONDON_CLOSE": (time(10, 0), time(12, 0), False),
    "NY_PM": (time(13, 30), time(16, 0), False),
}


@dataclass(frozen=True)
class Window:
    name: str
    start: datetime  # aware, owner tz
    end: datetime

    def contains(self, t: datetime) -> bool:
        return self.start <= t < self.end

    def label(self) -> str:
        return f"{self.name} {self.start:%H:%M}-{self.end:%H:%M}"


def windows_for(trading_day: date, tz: str | ZoneInfo = SAST) -> List[Window]:
    """Kill-zone windows for one NY trading day, expressed in ``tz``.

    The Asian zone (20:00-00:00 NY) belongs to the *previous* NY evening.
    """
    out_tz = ZoneInfo(tz) if isinstance(tz, str) else tz
    res = []
    for name, (s, e, prev) in KILL_ZONES.items():
        sd = trading_day - timedelta(days=1) if prev else trading_day
        start = datetime.combine(sd, s, NY)
        end = datetime.combine(sd if e > s else sd + timedelta(days=1), e, NY)
        res.append(Window(name, start.astimezone(out_tz), end.astimezone(out_tz)))
    return res


def active_kill_zones(t: datetime, tz: str | ZoneInfo = SAST) -> List[Window]:
    """All kill zones containing aware time ``t`` (Silver Bullet overlaps London Close)."""
    ny_day = t.astimezone(NY).date()
    found = []
    for d in (ny_day, ny_day + timedelta(days=1)):  # Asian zone of the next NY day starts this evening
        found += [w for w in windows_for(d, tz) if w.contains(t)]
    return found


def primary_kill_zone(t: datetime) -> Optional[str]:
    zs = active_kill_zones(t)
    return zs[0].name if zs else None


def schedule_crons() -> dict:
    """EventBridge Scheduler cron expressions in America/New_York (ScheduleExpressionTimezone).

    Every 5 minutes inside each kill zone, Mon-Fri (Asian zone runs Sun-Thu evenings NY).
    """
    return {
        "ASIAN": "cron(0/5 20-23 ? * SUN-THU *)",
        "LONDON_OPEN": "cron(0/5 2-4 ? * MON-FRI *)",
        "NY_AM": "cron(0/5 7-9 ? * MON-FRI *)",
        "SILVER_BULLET_LONDON_CLOSE": "cron(0/5 10-11 ? * MON-FRI *)",
        "NY_PM_1": "cron(30/5 13 ? * MON-FRI *)",
        "NY_PM_2": "cron(0/5 14-15 ? * MON-FRI *)",
    }
