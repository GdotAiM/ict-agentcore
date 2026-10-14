"""Decimal half-up rounding for risk / R maths."""
from ict_pipeline import money


def test_half_up_not_bankers():
    assert money.q(2.345, 2) == 2.35 and money.q(2.355, 2) == 2.36
    assert round(2.675, 2) == 2.67 and money.q(2.675, 2) == 2.68


def test_rr_and_size():
    assert money.q(money.rr(30425.1, 30361.7, 30665.0, "long"), 2) == 3.78
    assert money.position_size(10000, 0.5, 4105.34, 4117.60, 100.0) == 0.04
    assert money.position_size(None, 0.5, 1, 0, 1) is None   # equity never hard-coded
    assert money.exp_r(0.5, 2.0) == 0.5
