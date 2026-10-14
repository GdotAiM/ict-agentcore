"""Replay mode (acceptance test 15): run the full pipeline over 14 Oct 2026 with NO live data and
NO sending. Data = recorded OANDA 1m CSVs (tests/fixtures/replay_1m); agents = deterministic
ReplayLLM built from the reference markdown (stands in for Bedrock); DynamoDB = moto.

    python -m ict_pipeline.replay [--start 13:00 --end 16:00 --step 5]
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List
from zoneinfo import ZoneInfo

from .config import Settings
from .data_service import DataService, ReplayProvider
from .news import NewsCalendar, load_calendar
from .notifier import NullNotifier
from .observability import TokenBudget
from .reference_parser import RefTrade, load_reference

SAST = ZoneInfo("Africa/Johannesburg")
ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "replay_1m"


class ReplayLLM:
    """Deterministic stand-in for the Bedrock agents. Market-read outputs are computed from the
    shared snapshot; setup finders re-emit the reference trades in the cycle they were alerted."""

    def __init__(self, ref: dict, data: DataService, tokens: int = 500):
        self.ref, self.data, self.tokens = ref, data, tokens
        self.now: datetime | None = None
        self.emitted: set = set()

    def _env(self, agent, run_id, snap, instruments):
        return {"agent": agent, "run_id": run_id, "as_of": snap.as_of.isoformat(), "data_source": snap.data_source,
                "fallback_used": snap.fallback_used, "instruments": instruments, "notes": "replay", "errors": []}

    def invoke(self, agent: str, prompt: str):
        snap = self.data.snapshot(self.now)
        run_id = json.loads(prompt[prompt.index("{"):prompt.rindex("}") + 1]).get("run_id", "replay")
        bias = self.ref["bias_1533"] if self.now.strftime("%H:%M") >= "15:33" else self.ref["bias_1453"]
        if agent == "bias":
            inst = {}
            for s, tfs in snap.bars.items():
                d = tfs["1m"]
                hi, lo = max(b.high for b in d), min(b.low for b in d)
                last = d[-1].close
                eq = (hi + lo) / 2
                inst[s] = {"bias": bias.get(s, "neutral"), "confidence": 0.6, "dealing_range": {"high": hi, "low": lo},
                           "zone": "premium" if last > eq else "discount", "draw_on_liquidity": lo if bias.get(s) == "bearish" else hi,
                           "invalidation": None, "weekly_profile": "", "reason": "reference bias.md"}
            return json.dumps(self._env(agent, run_id, snap, inst)), self.tokens
        if agent == "timeframe":
            inst = {s: {"per_tf": {"D": {"dir": {"bullish": "bull", "bearish": "bear"}.get(bias.get(s), "range")}},
                        "aligned": False, "in_control": "D", "pairing": "D-15m-1m", "conflicts": []} for s in snap.bars}
            return json.dumps(self._env(agent, run_id, snap, inst)), self.tokens
        if agent == "intermarket":
            dxy = snap.bars.get("DXY", {}).get("15m", [])
            d = "up" if dxy and dxy[-1].close > dxy[-1].open else "down"
            inst = {"DXY": {"dxy_dir": d, "yields_dir": "flat", "risk": "off" if d == "up" else "on", "smt": [],
                            "supports": "short" if d == "up" else "long", "reason": "15m DXY candle"}}
            return json.dumps(self._env(agent, run_id, snap, inst)), self.tokens
        if agent == "liquidity":
            inst = {}
            for s, tfs in snap.bars.items():
                d = tfs["1m"]
                inst[s] = {"pools": [
                    {"id": f"{s}-DAY_L", "type": "SWING", "tf": "1m", "price": min(b.low for b in d), "status": "resting"},
                    {"id": f"{s}-DAY_H", "type": "SWING", "tf": "1m", "price": max(b.high for b in d), "status": "resting"}]}
            return json.dumps(self._env(agent, run_id, snap, inst)), self.tokens
        if agent == "orderflow":
            inst = {}
            for s, tfs in snap.bars.items():
                b = tfs["15m"][-1]
                inst[s] = {"per_tf": {"15m": {"flow": "bull" if b.close >= b.open else "bear", "evidence": "last 15m"}},
                           "agrees_with_bias": (b.close >= b.open) == (bias.get(s) == "bullish")}
            return json.dumps(self._env(agent, run_id, snap, inst)), self.tokens
        if agent in ("entry_model", "scalp", "pingpong"):
            cands = []
            for t in self.ref["trades"]:
                at = datetime.fromisoformat(t.alerted_at)
                if t.agent == agent and t.trade_id not in self.emitted and at <= self.now:
                    self.emitted.add(t.trade_id)
                    cands.append(_cand(t))
            out = {"agent": agent, "run_id": run_id, "as_of": snap.as_of.isoformat(), "data_source": snap.data_source,
                   "fallback_used": snap.fallback_used, "candidates": cands, "notes": "replay", "errors": []}
            return json.dumps(out), self.tokens
        if agent == "mentor":
            raise RuntimeError("mentor uses deterministic renderer in replay")
        raise RuntimeError(agent)


def _cand(t: RefTrade) -> dict:
    from . import money
    return {"candidate_id": t.trade_id, "agent": t.agent, "model": t.model, "instrument": t.instrument,
            "direction": t.direction, "tf": t.tf, "order": "limit", "entry": t.entry, "stop": t.stop, "tp1": t.tp1,
            "tp2": None, "raid_extreme": t.raid_extreme, "sweep_level_id": "", "mss_time": t.mss_time,
            "confirmation": "MSS+FVG", "rr_tp1": money.q(money.rr(t.entry, t.stop, t.tp1, t.direction), 2),
            "counter_trend": t.counter_trend, "valid_until": "2026-10-14T16:00:00+02:00",
            "early_exit": t.early_exit, "reason": t.notes[:200]}


def run_replay(start="13:00", end="16:00", step=5, settings: Settings | None = None, fixtures=FIXTURES,
               table_name="ict-replay-trade-state"):
    import boto3
    from moto import mock_aws
    from .agents.mentor import MentorAgent
    from .orchestrator import Pipeline
    from .trade_state import TradeStateWriter, create_table

    os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
    os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
    os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
    os.environ["EMF_STDOUT"] = "false"
    s = settings or Settings(owner_name=os.environ.get("OWNER_NAME", "owner"), replay=True,
                             log_dir="out/replay/logs", alert_dir="out/replay/alerts")
    with mock_aws():
        ddb = boto3.resource("dynamodb", region_name="us-east-1")
        create_table(ddb, table_name)
        writer = TradeStateWriter(table_name, ddb)
        data = DataService([ReplayProvider(str(fixtures))])
        cal = NewsCalendar(load_calendar(str(ROOT / "ict_pipeline/data/news_calendar.json")))
        ref = load_reference(ROOT / "reference")
        llm = ReplayLLM(ref, data)
        notifier = NullNotifier()
        pipe = Pipeline(s, data, writer, cal, notifier, TokenBudget(10**9), llm=llm,
                        mentor=MentorAgent(llm=None, owner=s.owner_name))
        t = datetime.fromisoformat(f"2026-10-14T{start}:00+02:00")
        t_end = datetime.fromisoformat(f"2026-10-14T{end}:00+02:00")
        results = []
        while t <= t_end:
            llm.now = t
            results.append(pipe.run_cycle(t))
            t += timedelta(minutes=step)
        trades = writer.all()
    return {"cycles": results, "trades": trades, "outbox": notifier.outbox}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="13:00"); ap.add_argument("--end", default="16:00")
    ap.add_argument("--step", type=int, default=5)
    a = ap.parse_args()
    r = run_replay(a.start, a.end, a.step)
    print(f"cycles={len(r['cycles'])} messages_built(not sent)={len(r['outbox'])}")
    for t in r["trades"]:
        print(f"{t['trade_id']:4s} {t['instrument']:7s} {t['direction']:5s} status={t['status']:9s} "
              f"fill={t.get('fill_time')} close={t.get('close_time')} R={t.get('result_r')} reason={t.get('exit_reason')}")
    blocked = [(b["candidate_id"], b["reason"]) for c in r["cycles"] for b in c["call"]["blocked"]]
    print("blocked:", blocked)
    os.makedirs("out/replay", exist_ok=True)
    with open("out/replay/summary.json", "w") as f:
        json.dump({"trades": r["trades"], "blocked": blocked}, f, indent=2, default=str)


if __name__ == "__main__":
    main()
