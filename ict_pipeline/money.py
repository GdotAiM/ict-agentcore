"""Decimal half-up maths for risk / R (NovaMart pattern: Decimal, round ONCE at the end)."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Optional


def D(x) -> Decimal:
    return Decimal(str(x))


def q(x, places: int = 2) -> float:
    return float(D(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def rr(entry, stop, target, direction: str) -> Decimal:
    risk = (D(entry) - D(stop)) if direction == "long" else (D(stop) - D(entry))
    reward = (D(target) - D(entry)) if direction == "long" else (D(entry) - D(target))
    if risk <= 0:
        return Decimal(0)
    return reward / risk


def r_multiple(entry, stop, exit_price, direction: str) -> float:
    return q(rr(entry, stop, exit_price, direction), 2)


def position_size(equity: Optional[float], risk_pct, entry, stop, value_per_point) -> Optional[float]:
    """lots = equity * risk% / (stop distance * value per point). None when equity unknown."""
    if equity is None or not value_per_point:
        return None
    dist = abs(D(entry) - D(stop))
    if dist == 0:
        return None
    lots = D(equity) * D(risk_pct) / Decimal(100) / (dist * D(value_per_point))
    return float(lots.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def exp_r(p_win: Optional[float], rr_val) -> Optional[float]:
    if p_win is None:
        return None
    return q(D(p_win) * D(rr_val) - (1 - D(p_win)), 2)
