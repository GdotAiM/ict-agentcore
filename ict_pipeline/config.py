"""Central configuration. Everything owner-specific comes from the environment (.env), never the repo.

Like NovaMart's config.py, AWS resource names resolve LAZILY from CloudFormation exports
(stack ``${PROJECT_NAME}``) with env-var overrides, so importing this module makes no AWS call
and the offline test-suite runs without credentials.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # pragma: no cover
    pass

SAST_TZ = "Africa/Johannesburg"
NY_TZ = "America/New_York"
INSTRUMENTS = ("NAS100", "XAUUSD", "EURUSD", "GBPUSD", "DXY")
TRADABLE = ("NAS100", "XAUUSD", "EURUSD", "GBPUSD")

# Contract maths per instrument (CFD-style, 1.0 lot). point = minimum price unit used for R maths.
# value_per_point = account-currency value of a 1.0 price-unit move for 1.0 lot.
INSTRUMENT_SPECS = {
    "NAS100": {"tv": ("NAS100USD", "OANDA"), "yf": ["NQ=F", "^NDX"], "value_per_point": 1.0, "spread": 1.5, "tick": 0.1},
    "XAUUSD": {"tv": ("XAUUSD", "OANDA"), "yf": ["GC=F"], "value_per_point": 100.0, "spread": 0.35, "tick": 0.01},
    "EURUSD": {"tv": ("EURUSD", "OANDA"), "yf": ["EURUSD=X"], "value_per_point": 100000.0, "spread": 0.00012, "tick": 0.00001},
    "GBPUSD": {"tv": ("GBPUSD", "OANDA"), "yf": ["GBPUSD=X"], "value_per_point": 100000.0, "spread": 0.00015, "tick": 0.00001},
    "DXY": {"tv": ("DXY", "TVC"), "yf": ["DX-Y.NYB"], "value_per_point": 0.0, "spread": 0.0, "tick": 0.001},
}
INTERMARKET_EXTRA = {"US10Y": (("US10Y", "TVC"), ["^TNX"]), "US02Y": (("US02Y", "TVC"), []), "ES": (("ES1!", "CME_MINI"), ["ES=F"])}

# Default correlated-risk grouping (rule 3). Key "INSTRUMENT:direction" -> unit id.
DEFAULT_RISK_GROUPS = {
    "EURUSD:long": "SHORT_USD", "GBPUSD:long": "SHORT_USD", "XAUUSD:long": "SHORT_USD", "DXY:short": "SHORT_USD",
    "EURUSD:short": "LONG_USD", "GBPUSD:short": "LONG_USD", "XAUUSD:short": "LONG_USD", "DXY:long": "LONG_USD",
    "NAS100:long": "NAS", "NAS100:short": "NAS",
}

ORCHESTRATOR_MODEL_ID = os.environ.get("ORCHESTRATOR_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0")
WORKER_MODEL_ID = os.environ.get("WORKER_MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")


class ConfigError(RuntimeError):
    pass


def _env_float(name: str, default: Optional[float]) -> Optional[float]:
    v = os.environ.get(name, "")
    return float(v) if v.strip() else default


@dataclass
class Settings:
    """Runtime settings. Build with ``Settings.from_env()``; tests construct it directly."""
    owner_name: str = "owner"
    owner_tz: str = SAST_TZ
    equity: Optional[float] = None            # never hard-coded; None => size shown as formula only
    account_currency: str = "USD"
    risk_pct: float = 0.5                     # percent of equity per risk unit (rule 2)
    min_rr: float = 2.0                       # rule 1
    wick_lookback: int = 60                   # rule 5 (N closed 1m candles)
    shared_unit_mode: str = "block"           # rule 3: "block" -> RISK_UNIT_FULL, "split" -> 0 extra risk
    risk_groups: dict = field(default_factory=lambda: dict(DEFAULT_RISK_GROUPS))
    news_pre_block_min: int = 15              # rule 7
    news_flat_min: int = 5
    scalp_post_block_min: int = 15
    cycle_minutes: int = 5
    daily_token_budget: int = 2_000_000
    budget_degrade_at: float = 0.90           # rule-of-section-8 / test 16
    notifier: str = "file"                    # file | telegram | email (stubs never send)
    alert_dir: str = "out/alerts"
    log_dir: str = "out/logs"
    calendar_path: str = "ict_pipeline/data/news_calendar.json"
    spreads: dict = field(default_factory=lambda: {k: v["spread"] for k, v in INSTRUMENT_SPECS.items()})
    trace_url_template: str = ""              # e.g. CloudWatch/X-Ray console URL with {run_id}
    replay: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        s = cls()
        s.owner_name = os.environ.get("OWNER_NAME", s.owner_name)
        s.owner_tz = os.environ.get("OWNER_TZ", s.owner_tz)
        s.equity = _env_float("EQUITY", None)
        s.account_currency = os.environ.get("ACCOUNT_CURRENCY", s.account_currency)
        s.risk_pct = _env_float("RISK_PCT", s.risk_pct)
        s.shared_unit_mode = os.environ.get("SHARED_UNIT_MODE", s.shared_unit_mode)
        if os.environ.get("RISK_GROUPS_JSON"):
            s.risk_groups.update(json.loads(os.environ["RISK_GROUPS_JSON"]))
        s.daily_token_budget = int(os.environ.get("DAILY_TOKEN_BUDGET", s.daily_token_budget))
        s.notifier = os.environ.get("ALERT_CHANNEL", s.notifier)
        s.alert_dir = os.environ.get("ALERT_DIR", s.alert_dir)
        s.log_dir = os.environ.get("LOG_DIR", s.log_dir)
        s.calendar_path = os.environ.get("NEWS_CALENDAR_PATH", s.calendar_path)
        s.trace_url_template = os.environ.get("TRACE_URL_TEMPLATE", s.trace_url_template)
        if os.environ.get("SPREADS_JSON"):
            s.spreads.update(json.loads(os.environ["SPREADS_JSON"]))
        return s


# ── AWS resource names (lazy CloudFormation exports, NovaMart pattern) ──────────────────────────
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
PROJECT_NAME = os.environ.get("PROJECT_NAME", "ict-agentcore")
_exports: Optional[dict] = None


def _cf_exports() -> dict:
    global _exports
    if _exports is None:
        import boto3
        cf = boto3.client("cloudformation", region_name=AWS_REGION)
        _exports = {e["Name"]: e["Value"] for p in cf.get_paginator("list_exports").paginate() for e in p["Exports"]}
    return _exports


def resource(key: str, env: str) -> str:
    """Env var wins; else CloudFormation export ``${PROJECT_NAME}-${key}``."""
    if os.environ.get(env):
        return os.environ[env]
    try:
        v = _cf_exports().get(f"{PROJECT_NAME}-{key}")
    except Exception as exc:  # no creds / no stack
        raise ConfigError(f"Cannot resolve {key}: set {env} or deploy the stack ({exc})") from exc
    if not v:
        raise ConfigError(f"CloudFormation export {PROJECT_NAME}-{key} missing; set {env}")
    return v


def trade_state_table() -> str:
    return resource("TradeStateTable", "TRADE_STATE_TABLE")


def ops_table() -> str:
    return resource("OpsTable", "OPS_TABLE")


def snapshot_bucket() -> str:
    return resource("SnapshotBucket", "SNAPSHOT_BUCKET")


GUARDRAIL_ID = os.environ.get("GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.environ.get("GUARDRAIL_VERSION", "")
RULES_KB_ID = os.environ.get("RULES_KB_ID", "")
TRANSCRIPTS_KB_ID = os.environ.get("TRANSCRIPTS_KB_ID", "")
AGENTCORE_MEMORY_ID = os.environ.get("AGENTCORE_MEMORY_ID", "")
AGENT_LOG_GROUP = os.environ.get("AGENT_LOG_GROUP", f"/aws/bedrock/agentcore/{PROJECT_NAME}")

if __name__ == "__main__":  # pragma: no cover
    s = Settings.from_env()
    print(json.dumps({k: v for k, v in s.__dict__.items()}, indent=2, default=str))
    for k, e in [("TradeStateTable", "TRADE_STATE_TABLE"), ("OpsTable", "OPS_TABLE"), ("SnapshotBucket", "SNAPSHOT_BUCKET"),
                 ("KbBucket", "KB_BUCKET"), ("VectorBucketArn", "VECTOR_BUCKET_ARN"), ("AgentCoreRoleArn", "AGENTCORE_ROLE_ARN")]:
        try:
            print(f"{k:18s} {resource(k, e)}")
        except ConfigError as exc:
            print(f"{k:18s} UNRESOLVED ({exc})")
