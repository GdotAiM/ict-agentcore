import json
from pathlib import Path

from ict_pipeline.agents.base import MockLLM
from ict_pipeline.agents.mentor import MentorAgent
from ict_pipeline.data_service import DataService, ReplayProvider
from ict_pipeline.notifier import NullNotifier
from ict_pipeline.observability import TokenBudget
from ict_pipeline.orchestrator import Pipeline

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures" / "replay_1m"


def _payload(prompt: str) -> dict:
    return json.loads(prompt[prompt.index("{"):prompt.rindex("}") + 1])


def envelope(agent, instruments_fn):
    def f(prompt):
        p = _payload(prompt)
        return {"agent": agent, "run_id": p["run_id"], "as_of": p["as_of"], "data_source": p["data_source"],
                "fallback_used": p["fallback_used"], "instruments": instruments_fn(p), "notes": "", "errors": []}
    return f


def finder(agent, cands):
    def f(prompt):
        p = _payload(prompt)
        return {"agent": agent, "run_id": p["run_id"], "as_of": p["as_of"], "data_source": p["data_source"],
                "fallback_used": p["fallback_used"], "candidates": cands, "notes": "", "errors": []}
    return f


def default_responses(bias="bearish"):
    rng = {"high": 31000.0, "low": 30000.0}
    return {
        "bias": envelope("bias", lambda p: {"NAS100": {"bias": bias, "confidence": 0.7, "dealing_range": rng,
                                                        "zone": "premium", "draw_on_liquidity": 30000.0,
                                                        "invalidation": 30720.0, "weekly_profile": "", "reason": "t"}}),
        "timeframe": envelope("timeframe", lambda p: {"NAS100": {"per_tf": {"D": {"dir": "bear"}}, "aligned": True,
                                                                  "in_control": "D", "pairing": "D-15m-1m", "conflicts": []}}),
        "intermarket": envelope("intermarket", lambda p: {"DXY": {"dxy_dir": "up", "yields_dir": "flat", "risk": "off",
                                                                   "smt": [], "supports": "short", "reason": "t"}}),
        "liquidity": envelope("liquidity", lambda p: {"NAS100": {"pools": [{"id": "P1", "type": "PDL", "tf": "15m",
                                                                            "price": 30401.2, "status": "swept"}]}}),
        "orderflow": envelope("orderflow", lambda p: {"NAS100": {"per_tf": {"1H": {"flow": "bear"}}, "agrees_with_bias": True}}),
        "entry_model": finder("entry_model", []),
        "scalp": finder("scalp", []),
        "pingpong": finder("pingpong", []),
    }


def make_pipeline(settings, writer, calendar, responses=None, providers=None, budget=None, notifier=None):
    llm = MockLLM(responses or default_responses())
    data = DataService(providers or [ReplayProvider(str(FIX))])
    notifier = notifier or NullNotifier()
    pipe = Pipeline(settings, data, writer, calendar, notifier, budget or TokenBudget(10**9), llm=llm,
                    mentor=MentorAgent(llm=None, owner=settings.owner_name))
    return pipe, llm, notifier
