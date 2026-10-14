"""Probability base rates from ``reference/findings/time_patterns.md`` (SPEC section 11).

Never invents numbers. Unknown models return ``p_win=None`` with ``base_rate_source`` explaining why.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class BaseRate:
    p_win: Optional[float]
    exp_r: Optional[float]
    n: int
    source: str
    status: str   # CONFIRMED | PROMISING | REJECTED | UNPROVEN
    small_sample: bool


# Keys: (model, instrument|ANY, confirmation|ANY)
RATES: Dict[tuple, BaseRate] = {
    ("PingPong", "ANY", "Unicorn"): BaseRate(0.55, 0.37, 30, "time_patterns: Ping-Pong Unicorn R:R>=2 (OANDA +0.37R n=30)", "PROMISING", True),
    ("PingPong", "XAUUSD", "Unicorn"): BaseRate(0.52, 0.25, 36, "time_patterns: Ping-Pong Unicorn R:R>=2 (Dukascopy XAU +0.25R n=36)", "PROMISING", False),
    ("PingPong", "ANY", "ANY"): BaseRate(0.48, -0.02, 195, "time_patterns: Ping-Pong overall OANDA -0.02R n=195", "REJECTED", False),
    ("Classic", "ANY", "ANY"): BaseRate(0.42, -0.17, 29, "time_patterns: Ping-Pong Classic OANDA -0.17R n=29", "REJECTED", True),
    ("Gold2", "XAUUSD", "ANY"): BaseRate(0.55, 0.50, 38, "time_patterns: Gold 2.0 FVG-midpoint +0.50R n=38", "CONFIRMED", False),
    ("FVG", "ANY", "ANY"): BaseRate(None, None, 37, "time_patterns: London sweep+MSS+FVG -0.14R n=37 (REJECTED)", "REJECTED", False),
    ("SilverBullet", "ANY", "ANY"): BaseRate(None, None, 8, "time_patterns: Silver Bullet -0.25R n=8 (too few)", "REJECTED", True),
    ("NASMacro", "NAS100", "ANY"): BaseRate(0.62, 0.19, 63, "time_patterns: NAS100 09:50-10:10 NY macro OOS +0.16-0.19R n=63", "PROMISING", False),
    ("OTE", "ANY", "ANY"): BaseRate(None, None, 0, "time_patterns: no confirmed OTE base rate", "UNPROVEN", True),
    ("IFVG", "ANY", "ANY"): BaseRate(None, None, 0, "time_patterns: no confirmed IFVG base rate", "UNPROVEN", True),
    ("OB", "ANY", "ANY"): BaseRate(None, None, 0, "time_patterns: no confirmed OB base rate", "UNPROVEN", True),
    ("Unicorn", "ANY", "ANY"): BaseRate(0.55, 0.37, 30, "time_patterns: Unicorn confirmation (Ping-Pong) +0.37R n=30", "PROMISING", True),
}


def lookup(model: str, instrument: str, confirmation: str = "") -> BaseRate:
    conf = "Unicorn" if "unicorn" in (confirmation or "").lower() else "ANY"
    for key in ((model, instrument, conf), (model, instrument, "ANY"), (model, "ANY", conf), (model, "ANY", "ANY")):
        if key in RATES:
            return RATES[key]
    return BaseRate(None, None, 0, f"no base rate for model={model}", "UNPROVEN", True)
