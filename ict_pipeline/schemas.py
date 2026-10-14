"""Strict JSON contracts (SPEC section 2). Invalid agent output is discarded and logged, never guessed."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Symbol = Literal["NAS100", "XAUUSD", "EURUSD", "GBPUSD", "DXY"]
Num = float  # validated in strict mode: strings are rejected


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


def _aware(v):
    if isinstance(v, str):
        v = datetime.fromisoformat(v)
    if v.tzinfo is None:
        raise ValueError("timestamp must carry a UTC offset")
    return v


# ── market-read payloads ──────────────────────────────────────────────────────────────────────
class Range(Strict):
    high: Num
    low: Num


class BiasInstr(Strict):
    bias: Literal["bullish", "bearish", "neutral"]
    confidence: float = Field(ge=0, le=1)
    dealing_range: Range
    zone: Literal["premium", "discount", "eq"]
    draw_on_liquidity: Optional[Num] = None
    invalidation: Optional[Num] = None
    weekly_profile: str = ""
    reason: str = Field(default="", max_length=400)


class PdArray(Strict):
    type: Literal["FVG", "OB", "breaker", "IFVG", "BPR", "VI"]
    low: Num
    high: Num


class TfRead(Strict):
    dir: Literal["bull", "bear", "range"]
    pd_array: Optional[PdArray] = None
    zone: Optional[Literal["premium", "discount", "eq"]] = None


class TimeframeInstr(Strict):
    per_tf: Dict[Literal["M", "W", "D", "4H", "1H", "15m", "5m", "1m"], TfRead]
    aligned: bool
    in_control: str
    pairing: str
    conflicts: List[str] = []


class Smt(Strict):
    pair: str
    side: Literal["high", "low"]
    leader: str
    time: str


class IntermarketInstr(Strict):
    dxy_dir: Literal["up", "down", "flat"]
    yields_dir: Literal["up", "down", "flat"]
    risk: Literal["on", "off", "mixed"]
    smt: List[Smt] = []
    supports: Literal["long", "short", "none"]
    reason: str = ""


class Pool(Strict):
    id: str
    type: Literal["EQH", "EQL", "PDH", "PDL", "ASIA_H", "ASIA_L", "LON_H", "LON_L", "SWING", "PWH", "PWL", "SESSION_H", "SESSION_L"]
    tf: str
    price: Num
    touches: List[str] = []
    tolerance: Num = 0.0
    status: Literal["resting", "swept"]
    swept_at: Optional[str] = None
    distance: Optional[Num] = None


class LiquidityInstr(Strict):
    pools: List[Pool]


class FlowRead(Strict):
    flow: Literal["bull", "bear"]
    last_flip_level: Optional[Num] = None
    evidence: str = ""


class OrderFlowInstr(Strict):
    per_tf: Dict[str, FlowRead]
    agrees_with_bias: bool


PAYLOADS = {"bias": BiasInstr, "timeframe": TimeframeInstr, "intermarket": IntermarketInstr,
            "liquidity": LiquidityInstr, "orderflow": OrderFlowInstr}


class Envelope(Strict):
    agent: str
    run_id: str
    as_of: datetime
    data_source: str
    fallback_used: bool
    instruments: Dict[Symbol, dict]
    notes: str = Field(default="", max_length=300)
    errors: List[str] = []

    model_config = ConfigDict(extra="forbid", strict=False)  # timestamps arrive as ISO strings in JSON

    _as_of = field_validator("as_of")(classmethod(lambda cls, v: _aware(v)))

    @model_validator(mode="after")
    def _typed_payload(self):
        model = PAYLOADS.get(self.agent)
        if model is not None:
            self.instruments = {k: model.model_validate(v).model_dump() for k, v in self.instruments.items()}
        return self


# ── setup finders ─────────────────────────────────────────────────────────────────────────────
class Candidate(Strict):
    candidate_id: str
    agent: Literal["entry_model", "scalp", "pingpong"]
    model: Literal["FVG", "OTE", "SilverBullet", "Classic", "PingPong", "Unicorn", "IFVG", "OB", "Gold2", "NASMacro"]
    instrument: Literal["NAS100", "XAUUSD", "EURUSD", "GBPUSD"]
    direction: Literal["long", "short"]
    tf: str
    order: Literal["limit", "market"]
    entry: Num
    stop: Num
    tp1: Num
    tp2: Optional[Num] = None
    raid_extreme: Num
    sweep_level_id: str = ""
    mss_time: str
    confirmation: str = ""
    rr_tp1: Num
    counter_trend: bool
    valid_until: str = ""
    early_exit: str = ""
    reason: str = Field(default="", max_length=200)
    trade_id: Optional[str] = None   # set when this is an update of an existing trade

    @model_validator(mode="after")
    def _geometry(self):
        if self.direction == "long" and not (self.stop < self.entry < self.tp1):
            raise ValueError("long needs stop < entry < tp1")
        if self.direction == "short" and not (self.stop > self.entry > self.tp1):
            raise ValueError("short needs stop > entry > tp1")
        _aware(self.mss_time)
        return self


class FinderOutput(Strict):
    agent: Literal["entry_model", "scalp", "pingpong"]
    run_id: str
    as_of: datetime
    data_source: str
    fallback_used: bool
    candidates: List[Candidate]
    notes: str = Field(default="", max_length=300)
    errors: List[str] = []
    model_config = ConfigDict(extra="forbid", strict=False)
    _as_of = field_validator("as_of")(classmethod(lambda cls, v: _aware(v)))


# ── checks ────────────────────────────────────────────────────────────────────────────────────
class Confluence(Strict):
    candidate_id: str
    score: int = Field(ge=1, le=5)
    agree: List[str] = []
    conflict: List[str] = []
    zone: Range | None = None


class Adjustment(Strict):
    factor: str
    delta: Num
    source: str


class Probability(Strict):
    candidate_id: str
    p_win: Optional[float] = Field(default=None, ge=0, le=1)
    ci: Optional[List[float]] = None
    exp_r: Optional[Num] = None
    n: Optional[int] = None
    small_sample: bool = True
    base_rate_source: Optional[str] = None
    adjustments: List[Adjustment] = []


class Citation(Strict):
    title: str
    url: str
    timestamp: str = ""


class Mentor(Strict):
    candidate_id: str
    model_match: bool
    time_ok: bool
    dol_ok: bool
    issues: List[str] = []
    citations: List[Citation] = []


# ── orchestrator output ───────────────────────────────────────────────────────────────────────
class TradeAlert(Strict):
    trade_id: str
    instrument: str
    direction: Literal["long", "short"]
    order: Literal["limit", "market"]
    entry: Num
    stop: Num
    tp1: Num
    rr: Num
    risk_unit: str
    risk_pct: Num
    size: Optional[Num] = None
    early_exit: str = ""
    counter_trend: bool
    confluence: Optional[int] = None
    p_win: Optional[float] = None
    exp_r: Optional[Num] = None
    sources: List[str] = []
    trace_url: str = ""
    notes: List[str] = []


class OpenTradeUpdate(Strict):
    trade_id: str
    status: str
    note: str


class Blocked(Strict):
    candidate_id: str
    reason: str
    detail: str = ""


class CombinedCall(Strict):
    run_id: str
    kill_zone: Optional[str]
    as_of: str
    headline: str
    market_summary: Dict[str, str] = {}
    trades: List[TradeAlert] = []
    open_trade_updates: List[OpenTradeUpdate] = []
    blocked: List[Blocked] = []
    data_source: str = ""
    fallback_used: bool = False
    degraded: bool = False
