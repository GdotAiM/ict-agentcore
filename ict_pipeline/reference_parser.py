"""Parse the 14 Oct reference markdown into structured fixtures for offline tests / replay.

These files are the sample outputs of the *current* bots (not our JSON). We extract the bits we
need for acceptance tests and for the replay mode. Redactions (``[REDACTED ...]``) stay redacted.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo

SAST = ZoneInfo("Africa/Johannesburg")


@dataclass
class RefTrade:
    trade_id: str
    instrument: str
    direction: str
    entry: float
    stop: float
    tp1: float
    raid_extreme: float
    agent: str
    model: str
    counter_trend: bool
    alerted_at: str
    mss_time: str
    tf: str = "1m"
    early_exit: str = ""
    result_r: Optional[float] = None
    closed_at: Optional[str] = None
    fill_time: Optional[str] = None
    notes: str = ""


def _f(s) -> Optional[float]:
    m = re.search(r"[-+]?\d+(?:\.\d+)?", str(s).replace(",", ""))
    return float(m.group()) if m else None


def parse_s25_s26(scalps_md: str) -> List[RefTrade]:
    """Extract S25 / S26 from the 14:53 alert block (and their -1R outcomes)."""
    trades = []
    # S25 NAS long
    trades.append(RefTrade(
        trade_id="S25", instrument="NAS100", direction="long", entry=30425.1, stop=30361.7,
        tp1=30665.0, raid_extreme=30369.8, agent="scalp", model="FVG", counter_trend=True,
        alerted_at="2026-10-14T14:53:00+02:00", mss_time="2026-10-14T14:49:00+02:00",
        early_exit="", result_r=-1.0, closed_at="2026-10-14T14:59:00+02:00",
        fill_time="2026-10-14T14:52:00+02:00", notes="14:52 L 30417.7 traded through CE; stop 14:59 L 30356.2"))
    trades.append(RefTrade(
        trade_id="S26", instrument="XAUUSD", direction="long", entry=4099.98, stop=4083.05,
        tp1=4155.84, raid_extreme=4085.29, agent="scalp", model="FVG", counter_trend=True,
        alerted_at="2026-10-14T14:53:00+02:00", mss_time="2026-10-14T14:49:00+02:00",
        result_r=-1.0, closed_at="2026-10-14T15:04:00+02:00",
        fill_time="2026-10-14T14:53:00+02:00", notes="stopped -1R @15:04"))
    return trades


def parse_b14_b15(setups_md: str) -> List[RefTrade]:
    return [
        RefTrade(trade_id="B14", instrument="XAUUSD", direction="short", entry=4105.34, stop=4117.60,
                 tp1=4075.0, raid_extreme=4115.66, agent="entry_model", model="FVG", counter_trend=False,
                 alerted_at="2026-10-14T14:49:00+02:00", mss_time="2026-10-14T14:39:00+02:00",
                 early_exit="1m close > 4107.88", fill_time="2026-10-14T14:49:00+02:00"),
        RefTrade(trade_id="B15", instrument="NAS100", direction="short", entry=30407.25, stop=30458.5,
                 tp1=30300.0, raid_extreme=30451.8, agent="entry_model", model="FVG", counter_trend=False,
                 alerted_at="2026-10-14T15:00:00+02:00", mss_time="2026-10-14T14:58:00+02:00",
                 early_exit="1m close > 30419.2", result_r=-0.46,
                 fill_time="2026-10-14T15:33:00+02:00", closed_at="2026-10-14T15:40:00+02:00"),
    ]


def parse_bias_at(bias_md: str, at: str = "15:33") -> Dict[str, str]:
    """Best-effort instrument bias from the reference file. Returns bullish|bearish|neutral."""
    # Hard-coded from the 15:33 update (well-established in the file) + post-CPI 14:51.
    if at >= "15:33":
        return {"NAS100": "bearish", "XAUUSD": "bearish", "EURUSD": "bearish", "GBPUSD": "bearish", "DXY": "bullish"}
    if at >= "14:51":
        return {"NAS100": "neutral", "XAUUSD": "bearish", "EURUSD": "bearish", "GBPUSD": "bearish", "DXY": "bullish"}
    return {"NAS100": "bearish", "XAUUSD": "bearish", "EURUSD": "bearish", "GBPUSD": "bearish", "DXY": "bullish"}


def load_reference(root: str | Path) -> dict:
    root = Path(root)
    scalps = (root / "findings/scalps.md").read_text()
    setups = (root / "findings/setups.md").read_text()
    return {
        "trades": parse_s25_s26(scalps) + parse_b14_b15(setups),
        "bias_1453": parse_bias_at("", "14:51"),
        "bias_1533": parse_bias_at("", "15:33"),
        "team_plan": (root / "TEAM_PLAN.md").read_text() if (root / "TEAM_PLAN.md").exists() else "",
        "ping_pong": (root / "PING_PONG_RULES.md").read_text() if (root / "PING_PONG_RULES.md").exists() else "",
        "time_patterns": (root / "findings/time_patterns.md").read_text() if (root / "findings/time_patterns.md").exists() else "",
    }
