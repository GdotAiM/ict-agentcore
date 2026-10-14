"""Optimistic locking (expected_version), conditional writes, single writer, append-only history."""
import pytest
from conftest import T
from ict_pipeline.trade_state import (IllegalTransition, TradeStateReader, TradeStateWriter, VersionConflict)

ROW = {"trade_id": "B14", "instrument": "XAUUSD", "direction": "short", "entry": 4105.34, "stop": 4117.6,
       "tp1": 4075.0, "risk_unit": "LONG_USD", "risk_pct": 0.5}


def test_create_is_conditional(writer):
    writer.create(ROW, T("14:49"))
    with pytest.raises(VersionConflict):
        writer.create(ROW, T("14:50"))


def test_expected_version_enforced(writer):
    writer.create(ROW, T("14:49"))
    writer.transition("B14", "filled", 0, T("14:49"), fill_price=4105.34)
    with pytest.raises(VersionConflict):              # stale version
        writer.transition("B14", "closed", 0, T("15:00"), exit_reason="stop")
    t = writer.transition("B14", "closed", 1, T("15:00"), exit_reason="tp1", result_r=2.47)
    assert t["version"] == 2 and [h["status"] for h in t["history"]] == ["pending", "filled", "closed"]


def test_illegal_transition(writer):
    writer.create(ROW, T("14:49"))
    with pytest.raises(IllegalTransition):
        writer.transition("B14", "closed", 0, T("14:50"))


def test_single_writer(ddb, writer):
    with pytest.raises(PermissionError):
        TradeStateWriter("ts-test", ddb, writer="scalp_agent")
    assert not hasattr(TradeStateReader("ts-test", ddb), "transition")


def test_stale_writer_loses_to_fresh_version(writer):
    """Optimistic lock: a writer holding an old expected_version loses (like two concurrent updates)."""
    writer.create(ROW, T("14:49"))
    # Writer A and B both read version 0
    a_ver = writer.get("B14")["version"]
    b_ver = writer.get("B14")["version"]
    assert a_ver == b_ver == 0
    writer.transition("B14", "filled", a_ver, T("14:50"), note="writer-A")   # A wins
    with pytest.raises(VersionConflict):
        writer.transition("B14", "filled", b_ver, T("14:50"), note="writer-B")  # B loses
    assert writer.transition_retry("B14", "closed", T("15:00"), note="retry")["version"] == 2
