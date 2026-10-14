import os, sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ["EMF_STDOUT"] = "false"
os.environ.pop("AGENTCORE_MEMORY_ID", None)

SAST = ZoneInfo("Africa/Johannesburg")


def T(hm: str, day: str = "2026-10-14") -> datetime:
    return datetime.fromisoformat(f"{day}T{hm}:00+02:00")


@pytest.fixture
def ddb():
    import boto3
    from moto import mock_aws
    with mock_aws():
        yield boto3.resource("dynamodb", region_name="us-east-1")


@pytest.fixture
def writer(ddb):
    from ict_pipeline.trade_state import TradeStateWriter, create_table
    create_table(ddb, "ts-test")
    return TradeStateWriter("ts-test", ddb)


@pytest.fixture
def settings(tmp_path):
    from ict_pipeline.config import Settings
    return Settings(owner_name="ntloso", equity=None, log_dir=str(tmp_path / "logs"), alert_dir=str(tmp_path / "alerts"))


@pytest.fixture
def calendar():
    from ict_pipeline.news import NewsCalendar, load_calendar
    return NewsCalendar(load_calendar(str(ROOT / "ict_pipeline/data/news_calendar.json")))


def flat_bars(symbol_price: float, start: datetime, n: int, wick: float = 1.0, step=0.0):
    from ict_pipeline.candles import Bar
    out = []
    p = symbol_price
    for i in range(n):
        out.append(Bar(start + timedelta(minutes=i), p, p + wick, p - wick, p))
        p += step
    return out


def cand(**kw):
    from ict_pipeline.schemas import Candidate
    base = dict(candidate_id="C1", agent="entry_model", model="FVG", instrument="NAS100", direction="long", tf="1m",
                order="limit", entry=100.0, stop=90.0, tp1=130.0, raid_extreme=92.0, sweep_level_id="",
                mss_time="2026-10-14T14:00:00+02:00", confirmation="MSS", rr_tp1=3.0, counter_trend=False,
                valid_until="", early_exit="", reason="")
    base.update(kw)
    return Candidate.model_validate(base)
