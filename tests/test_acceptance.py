"""SPEC section 12: the 16 acceptance tests, all offline (moto, fixtures, mocked LLM)."""
import socket
from datetime import date, timedelta

import pandas as pd
import pytest

from conftest import T, cand, flat_bars
from helpers import FIX, default_responses, finder, make_pipeline

from ict_pipeline import rules as R
from ict_pipeline.agents.base import AgentRunner, MockLLM, validate_envelope
from ict_pipeline.agents.mentor import render_deterministic
from ict_pipeline.data_service import DataService, DataUnavailable, ReplayProvider, YFinanceProvider
from ict_pipeline.fills import update_trades
from ict_pipeline.guardrails import FOOTER, filter_outbound
from ict_pipeline.killzones import windows_for
from ict_pipeline.news import NewsCalendar, NewsEvent
from ict_pipeline.observability import RunLog, TokenBudget
from ict_pipeline.rules import RuleEngine
from ict_pipeline.schemas import CombinedCall, TradeAlert
from ict_pipeline.trade_state import TradeStateReader


def engine(settings, calendar, **over):
    for k, v in over.items():
        setattr(settings, k, v)
    return RuleEngine(settings, calendar)


# 1 ─ Kill-zone clock across the DST switch ──────────────────────────────────────────────────
def test_01_kill_zone_clock_dst():
    exp = {
        date(2026, 10, 14): {"ASIAN": "02:00-06:00", "LONDON_OPEN": "08:00-11:00", "NY_AM": "13:00-16:00",
                             "SILVER_BULLET": "16:00-17:00", "LONDON_CLOSE": "16:00-18:00", "NY_PM": "19:30-22:00"},
        date(2026, 11, 3): {"ASIAN": "03:00-07:00", "LONDON_OPEN": "09:00-12:00", "NY_AM": "14:00-17:00",
                            "SILVER_BULLET": "17:00-18:00", "LONDON_CLOSE": "17:00-19:00", "NY_PM": "20:30-23:00"},
    }
    for d, zones in exp.items():
        got = {w.name: f"{w.start:%H:%M}-{w.end:%H:%M}" for w in windows_for(d)}
        assert got == zones
        asian = [w for w in windows_for(d) if w.name == "ASIAN"][0]
        assert asian.start.date() == d  # 20:00 NY previous day == early morning SAST same day


# 2 ─ Schema: malformed output discarded + logged, pipeline continues ─────────────────────────
def test_02_schema_malformed_discarded(settings, writer, calendar):
    resp = default_responses()
    good_bias = resp["bias"]

    def bad_bias(prompt):
        d = good_bias(prompt)
        d["instruments"]["NAS100"]["dealing_range"]["high"] = "31000"  # price as string -> invalid
        return d
    resp["bias"] = bad_bias
    pipe, llm, out = make_pipeline(settings, writer, calendar, resp)
    res = pipe.run_cycle(T("14:05"))
    calls = [r for r in res["log"] if r["kind"] == "agent_call"]
    bias = [r for r in calls if r["agent"] == "bias"][0]
    assert bias["valid"] is False and "ValidationError" in bias["error"]
    assert all(r["valid"] for r in calls if r["agent"] != "bias")
    assert len(out.outbox) == 1 and FOOTER in out.outbox[0]


# 3 ─ R:R after padding: 1.9 blocked, 2.0 passes ──────────────────────────────────────────────
def test_03_rr_threshold(settings, calendar):
    eng = engine(settings, calendar, spreads={"NAS100": 0.0})
    bars = {"NAS100": flat_bars(100.0, T("13:00"), 60, wick=0.0)}
    c19 = cand(candidate_id="A", entry=100.0, stop=90.0, tp1=119.0, raid_extreme=95.0, rr_tp1=1.9,
               mss_time=T("13:58").isoformat())
    c20 = cand(candidate_id="B", entry=200.0, stop=190.0, tp1=220.0, raid_extreme=195.0, rr_tp1=2.0,
               mss_time=T("13:58").isoformat())
    d = {x.candidate.candidate_id: x for x in eng.evaluate([c19, c20], T("14:00"), bars, [], {}, {})}
    assert d["A"].reason == R.RR_BELOW_2 and not d["A"].passed
    assert d["B"].passed and d["B"].rr == 2.0


# 4 ─ Stop padding moves stop; if R:R < 2 -> STOP_TOO_TIGHT ──────────────────────────────────
def test_04_stop_padding(settings, calendar):
    eng = engine(settings, calendar, spreads={"NAS100": 1.5})
    bars = {"NAS100": flat_bars(100.0, T("13:00"), 60, wick=2.0)}  # median lower wick = 2.0
    ok = cand(candidate_id="OK", entry=100.0, stop=91.0, tp1=130.0, raid_extreme=92.0, mss_time=T("13:58").isoformat())
    tight = cand(candidate_id="TIGHT", entry=200.0, stop=191.0, tp1=220.0, raid_extreme=192.0, rr_tp1=2.2,
                 mss_time=T("13:58").isoformat())
    d = {x.candidate.candidate_id: x for x in eng.evaluate([ok, tight], T("14:00"), {"NAS100": bars["NAS100"]}, [], {}, {})}
    assert d["OK"].passed and d["OK"].stop == pytest.approx(88.5)       # 92 - (1.5 + 2.0)
    assert d["TIGHT"].reason == R.STOP_TOO_TIGHT and d["TIGHT"].stop == pytest.approx(188.5)


# 5 ─ Shared risk unit (B14 XAU short open at 0.5%) ───────────────────────────────────────────
@pytest.mark.parametrize("mode,expect", [("block", R.RISK_UNIT_FULL), ("split", None)])
def test_05_shared_unit(settings, calendar, writer, mode, expect):
    writer.create({"trade_id": "B14", "instrument": "XAUUSD", "direction": "short", "entry": 4105.34, "stop": 4117.60,
                   "tp1": 4075.0, "risk_unit": "LONG_USD", "risk_pct": 0.5}, T("14:49"), status="pending")
    writer.transition_retry("B14", "filled", T("14:49"), fill_price=4105.34)
    eng = engine(settings, calendar, shared_unit_mode=mode, spreads={"EURUSD": 0.0})
    bars = {"EURUSD": flat_bars(1.113, T("14:00"), 60, wick=0.0)}
    c = cand(candidate_id="B16", instrument="EURUSD", direction="short", entry=1.113365, stop=1.11394, tp1=1.11142,
             raid_extreme=1.11374, rr_tp1=3.38, mss_time=T("15:42").isoformat())
    d = eng.evaluate([c], T("15:47"), bars, writer.active(), {}, {})[0]
    if expect:
        assert d.reason == expect
    else:
        assert d.passed and d.risk_pct == 0.0 and d.risk_unit == "LONG_USD"
        assert any("0% extra" in n for n in d.notes)


# 6 ─ Opposite direction on same instrument ────────────────────────────────────────────────────
def test_06_opposite_open(settings, calendar, writer):
    writer.create({"trade_id": "B15", "instrument": "NAS100", "direction": "short", "entry": 30407.25, "stop": 30458.5,
                   "tp1": 30300.0, "risk_unit": "NAS", "risk_pct": 0.5}, T("15:00"), status="pending")
    eng = engine(settings, calendar)
    c = cand(candidate_id="L1", entry=30400.0, stop=30300.0, tp1=30700.0, raid_extreme=30320.0,
             mss_time=T("15:10").isoformat())
    d = eng.evaluate([c], T("15:15"), {"NAS100": flat_bars(30400, T("14:00"), 60)}, writer.active(), {}, {})[0]
    assert d.reason == R.OPPOSITE_OPEN


# 7 ─ News: CPI 08:30 NY -> no fills after 14:15 SAST, flat/cancel at 14:25 ───────────────────
def test_07_news_blackout(settings, calendar, writer):
    eng = engine(settings, calendar)
    bars = {"NAS100": flat_bars(30600, T("13:00"), 80)}
    c = cand(entry=30600.0, stop=30500.0, tp1=30900.0, raid_extreme=30550.0, mss_time=T("14:12").isoformat())
    assert eng.evaluate([c], T("14:16"), bars, [], {}, {})[0].reason == R.NEWS_BLACKOUT
    assert eng.evaluate([c], T("14:14"), bars, [], {}, {})[0].passed
    # fill engine: pending order touched at 14:16 is cancelled, not filled
    writer.create({"trade_id": "P1", "instrument": "NAS100", "direction": "long", "entry": 30600.0, "stop": 30500.0,
                   "tp1": 30900.0, "risk_unit": "NAS", "risk_pct": 0.5}, T("14:16"))
    writer.create({"trade_id": "F1", "instrument": "XAUUSD", "direction": "short", "entry": 4140.0, "stop": 4160.0,
                   "tp1": 4100.0, "risk_unit": "LONG_USD", "risk_pct": 0.5}, T("14:00"))
    writer.transition_retry("F1", "filled", T("14:00"), fill_price=4140.0, last_bar=T("14:00").isoformat())
    data = {"NAS100": flat_bars(30600, T("14:10"), 20, wick=1.0), "XAUUSD": flat_bars(4135.0, T("14:10"), 20, wick=0.5)}
    update_trades(writer, data, T("14:30"), calendar)
    p1, f1 = writer.get("P1"), writer.get("F1")
    assert p1["status"] == "cancelled" and p1.get("fill_time") is None
    assert f1["status"] == "closed" and f1["exit_reason"] == "news_flat" and f1["close_time"].startswith("2026-10-14T14:25")
    # orchestrator emits the flat/cancel message at 14:25 for anything still open
    assert calendar.flat_time(calendar.events[0]).astimezone(T("14:00").tzinfo).strftime("%H:%M") == "14:25"
    assert calendar.no_fill_from(calendar.events[0]).astimezone(T("14:00").tzinfo).strftime("%H:%M") == "14:15"
    # Another test date across DST: CPI 08:30 NY on 2026-11-12 -> 15:15 / 15:25 SAST
    from zoneinfo import ZoneInfo
    from datetime import datetime
    ev = NewsEvent("US CPI", "USD", datetime(2026, 11, 12, 8, 30, tzinfo=ZoneInfo("America/New_York")))
    cal2 = NewsCalendar([ev])
    assert cal2.no_fill_from(ev).astimezone(ZoneInfo("Africa/Johannesburg")).strftime("%H:%M") == "15:15"
    assert cal2.flat_time(ev).astimezone(ZoneInfo("Africa/Johannesburg")).strftime("%H:%M") == "15:25"


def test_07b_flat_message_in_call(settings, calendar, writer):
    writer.create({"trade_id": "F2", "instrument": "NAS100", "direction": "short", "entry": 31000.0, "stop": 31100.0,
                   "tp1": 30000.0, "risk_unit": "NAS", "risk_pct": 0.5}, T("14:20"))
    pipe, _, out = make_pipeline(settings, writer, calendar)
    res = pipe.run_cycle(T("14:25"))
    assert any("close/cancel for US CPI" in u["note"] for u in res["call"]["open_trade_updates"])
    assert "close/cancel for US CPI" in out.outbox[0]


# 8 ─ Forming candle rejected ──────────────────────────────────────────────────────────────────
def test_08_forming_candle(settings, calendar):
    eng = engine(settings, calendar)
    now = T("14:00") + timedelta(seconds=30)
    c = cand(mss_time=T("14:00").isoformat())  # 14:00 1m bar closes 14:01
    assert eng.evaluate([c], now, {"NAS100": flat_bars(100, T("13:00"), 60)}, [], {}, {})[0].reason == R.FORMING_CANDLE
    c5 = cand(tf="5m", mss_time=T("13:56").isoformat())  # 13:55-14:00 5m bar would be closed; 13:56 start isn't
    assert eng.evaluate([c5], T("14:00"), {"NAS100": flat_bars(100, T("13:00"), 60)}, [], {}, {})[0].reason == R.FORMING_CANDLE
    # data service drops the forming bar too
    snap = DataService([ReplayProvider(str(FIX))]).snapshot(T("14:53") + timedelta(seconds=20))
    assert snap.bars["NAS100"]["1m"][-1].time == T("14:52")


# 9 ─ Counter-trend labelled in the message ─────────────────────────────────────────────────────
def test_09_counter_trend_label(settings, calendar):
    eng = engine(settings, calendar)
    c = cand(counter_trend=False, mss_time=T("13:58").isoformat())
    d = eng.evaluate([c], T("14:00"), {"NAS100": flat_bars(100, T("13:00"), 60, wick=0.1)}, [], {"NAS100": "bearish"}, {})[0]
    assert d.passed and d.counter_trend
    call = CombinedCall(run_id="r", kill_zone="NY_AM", as_of=T("14:00").isoformat(), headline="1 setup",
                        trades=[TradeAlert(trade_id="C1", instrument="NAS100", direction="long", order="limit",
                                           entry=100.0, stop=d.stop, tp1=130.0, rr=d.rr, risk_unit="NAS", risk_pct=0.5,
                                           counter_trend=d.counter_trend)])
    assert "COUNTER-TREND" in render_deterministic(call, "ntloso")


# 10 ─ Fills: replay 14 Oct real OANDA 1m -> S25 stopped -1R at 14:59 SAST ────────────────────
def test_10_s25_fill_replay(writer, calendar, ddb):
    from ict_pipeline.reference_parser import load_reference
    from conftest import ROOT
    s25 = [t for t in load_reference(ROOT / "reference")["trades"] if t.trade_id == "S25"][0]
    writer.create({"trade_id": "S25", "instrument": "NAS100", "direction": "long", "entry": s25.entry, "stop": s25.stop,
                   "tp1": s25.tp1, "risk_unit": "NAS", "risk_pct": 0.5, "valid_until": "2026-10-14T16:00:00+02:00"},
                  T("14:52"))
    data = DataService([ReplayProvider(str(FIX))])
    for minute in ["14:55", "15:00", "15:05"]:          # three monitor cycles
        update_trades(writer, data.snapshot(T(minute)).bars_1m(), T(minute), calendar)
    a = TradeStateReader("ts-test", ddb).get("S25")
    b = TradeStateReader("ts-test", ddb).get("S25")
    assert a == b                                          # consistent for all readers
    assert a["status"] == "closed" and a["result_r"] == -1.0 and a["exit_reason"] == "stop"
    assert a["fill_time"].startswith("2026-10-14T14:52") and a["close_time"].startswith("2026-10-14T14:59")
    assert [h["status"] for h in a["history"]][:3] == ["pending", "filled", "closed"]


def test_10b_same_candle_stop_first(writer):
    from ict_pipeline.candles import Bar
    writer.create({"trade_id": "X", "instrument": "NAS100", "direction": "long", "entry": 100.0, "stop": 95.0,
                   "tp1": 110.0, "risk_unit": "NAS", "risk_pct": 0.5}, T("14:00"))
    writer.transition_retry("X", "filled", T("14:00"), fill_price=100.0, last_bar=T("14:00").isoformat())
    update_trades(writer, {"NAS100": [Bar(T("14:01"), 100, 111, 94, 100)]}, T("14:03"))
    assert writer.get("X")["exit_reason"] == "stop" and writer.get("X")["result_r"] == -1.0


# 11 ─ Staleness ───────────────────────────────────────────────────────────────────────────────
def test_11_stale_output_rejected():
    def stale(prompt):
        return {"agent": "bias", "run_id": "r", "as_of": "2026-10-14T14:30:00+02:00", "data_source": "TV:OANDA",
                "fallback_used": False, "instruments": {}, "notes": "", "errors": []}
    log = RunLog("r")
    r = AgentRunner("bias", MockLLM({"bias": stale}), lambda x: validate_envelope(x, "bias"), log)
    res = r.run({"as_of": "x"}, T("14:45"))
    assert not res.ok and "stale" in res.error
    assert log.records[0]["valid"] is False


# 12 ─ One combined message, deduped ───────────────────────────────────────────────────────────
def test_12_one_message_deduped(settings, writer, calendar):
    mt = T("14:03").isoformat()
    def c(cid, agent, inst, d, e, s, tp, raid):
        return {"candidate_id": cid, "agent": agent, "model": "FVG", "instrument": inst, "direction": d, "tf": "1m",
                "order": "limit", "entry": e, "stop": s, "tp1": tp, "raid_extreme": raid, "mss_time": mt,
                "rr_tp1": 3.0, "counter_trend": False}
    resp = default_responses()
    resp["entry_model"] = finder("entry_model", [c("E1", "entry_model", "NAS100", "short", 30600.0, 30700.0, 30300.0, 30650.0),
                                                 c("E2", "entry_model", "XAUUSD", "short", 4150.0, 4170.0, 4100.0, 4160.0)])
    resp["scalp"] = finder("scalp", [c("S1", "scalp", "NAS100", "short", 30601.0, 30700.0, 30300.0, 30650.0),
                                     c("S2", "scalp", "NAS100", "short", 30605.0, 30700.0, 30300.0, 30650.0)])
    resp["pingpong"] = finder("pingpong", [c("P1", "pingpong", "XAUUSD", "short", 4150.5, 4170.0, 4100.0, 4160.0)])
    pipe, llm, out = make_pipeline(settings, writer, calendar, resp)
    res = pipe.run_cycle(T("14:05"))
    assert len(out.outbox) == 1
    ids = sorted(t["trade_id"] for t in res["call"]["trades"])
    assert len(ids) == 2
    dups = [b for b in res["call"]["blocked"] if b["reason"] == "DUPLICATE"]
    assert len(dups) == 3, res["call"]["blocked"]
    # next cycle: same candidates are updates, not new alerts
    res2 = pipe.run_cycle(T("14:10"))
    assert res2["call"]["trades"] == [] and len(out.outbox) == 2


# 13 ─ Guardrails ──────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("text", [
    "Place the order on NAS100 now",
    "here is my api_key: abcd1234efgh",
    "size the trade for my friend's account",
    "log into the broker account and buy",
])
def test_13_guardrails_block(text):
    allowed, cleaned, reasons = filter_outbound(text)
    assert not allowed and reasons


def test_13b_mentor_text_filtered():
    from ict_pipeline.agents.mentor import MentorAgent
    llm = MockLLM({"mentor": "Great setup. I will place the order for your friend's account."})
    call = CombinedCall(run_id="r", kill_zone="NY_AM", as_of=T("14:00").isoformat(), headline="No trade")
    msg = MentorAgent(llm=llm, owner="ntloso").compose(call)
    assert "place the order" not in msg.lower() and msg.rstrip().endswith(FOOTER)


# 14 ─ Fallback: TradingView down -> yfinance, fallback_used shown ─────────────────────────────
class DeadTV:
    name, is_fallback = "TV:OANDA", False
    def bars_1m(self, *a, **k):
        raise DataUnavailable("TradingView killed")


def fake_yf(sym):
    idx = pd.date_range("2026-10-14 11:00", periods=180, freq="1min", tz="UTC")
    return pd.DataFrame({"Open": 100.0, "High": 101.0, "Low": 99.0, "Close": 100.0}, index=idx)


def test_14_fallback(settings, writer, calendar):
    pipe, _, out = make_pipeline(settings, writer, calendar, providers=[DeadTV(), YFinanceProvider(fake_yf)])
    res = pipe.run_cycle(T("14:05"))
    assert res["call"]["fallback_used"] is True and res["call"]["data_source"] == "yfinance"
    assert "data: fallback" in out.outbox[0]


# 15 ─ Replay mode: whole pipeline, no live data, no sending ───────────────────────────────────
def test_15_replay_mode(monkeypatch):
    def no_net(*a, **k):
        raise AssertionError("network used in replay")
    monkeypatch.setattr(socket.socket, "connect", no_net)
    from ict_pipeline.replay import run_replay
    r = run_replay("13:00", "16:00", 5)
    assert len(r["cycles"]) == 37 and len(r["outbox"]) == 37
    assert all(c["notify"]["sent"] is False for c in r["cycles"])
    t = {x["trade_id"]: x for x in r["trades"]}
    assert t["S25"]["result_r"] == -1.0 and t["S25"]["close_time"].startswith("2026-10-14T14:59")
    assert t["B15"]["exit_reason"] == "early_exit" and t["B15"]["close_time"].startswith("2026-10-14T15:40")
    assert t["B14"]["status"] == "filled"
    blocked = {b["candidate_id"]: b["reason"] for c in r["cycles"] for b in c["call"]["blocked"]}
    assert blocked.get("S26") == "OPPOSITE_OPEN"   # gold long vs open B14 gold short (14 Oct lesson)
    assert all(m.rstrip().endswith(FOOTER) for m in r["outbox"])


# 16 ─ Budget degradation at 90% ───────────────────────────────────────────────────────────────
def test_16_budget_degradation(settings, writer, calendar):
    b = TokenBudget(limit=1000, degrade_at=0.9)
    b.add(900)
    writer.create({"trade_id": "S25", "instrument": "NAS100", "direction": "long", "entry": 30425.1, "stop": 30361.7,
                   "tp1": 30665.0, "risk_unit": "NAS", "risk_pct": 0.5}, T("14:52"))
    pipe, llm, out = make_pipeline(settings, writer, calendar, budget=b)
    res = pipe.run_cycle(T("15:00"))
    assert res["degraded"] is True and llm.calls == []          # no LLM agent ran
    assert writer.get("S25")["status"] == "closed"              # open-trade monitoring still ran
    assert "degraded" in out.outbox[0]
