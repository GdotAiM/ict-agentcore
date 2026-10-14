"""Market data service (SPEC section 4): fetch once per cycle, cache one snapshot, every agent reads it.

Providers: TradingView OANDA via tvDatafeed (primary) -> yfinance (fallback, ``fallback_used=True``)
-> replay CSV (offline). Only CLOSED bars are kept; ``last_closed_bar`` stored per symbol/TF.
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Protocol
from zoneinfo import ZoneInfo

from .candles import Bar, closed_only, resample
from .config import INSTRUMENT_SPECS, INSTRUMENTS, SAST_TZ

log = logging.getLogger(__name__)
SAST = ZoneInfo(SAST_TZ)


class DataUnavailable(RuntimeError):
    pass


class Provider(Protocol):
    name: str
    is_fallback: bool
    def bars_1m(self, symbol: str, now: datetime, n: int) -> List[Bar]: ...


class TradingViewProvider:
    name, is_fallback = "TV:OANDA", False

    def __init__(self, client=None):
        self._client = client

    def _tv(self):
        if self._client is None:
            from tvDatafeed import TvDatafeed  # no-login mode; no credentials anywhere
            self._client = TvDatafeed()
        return self._client

    def bars_1m(self, symbol, now, n=1000):
        from tvDatafeed import Interval
        sym, ex = INSTRUMENT_SPECS[symbol]["tv"]
        df = self._tv().get_hist(sym, ex, interval=Interval.in_1_minute, n_bars=n)
        if df is None or df.empty:
            raise DataUnavailable(f"TV returned nothing for {symbol}")
        out = []
        for ts, r in df.iterrows():
            t = ts.to_pydatetime()
            t = t.astimezone(SAST)  # tvDatafeed returns naive host-local time (UTC in AgentCore); astimezone treats naive as local
            out.append(Bar(t, float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])))
        return out


class YFinanceProvider:
    name, is_fallback = "yfinance", True

    def __init__(self, downloader=None):
        self._dl = downloader

    def bars_1m(self, symbol, now, n=1000):
        if self._dl is None:
            import yfinance as yf
            self._dl = lambda s: yf.download(s, period="5d", interval="1m", progress=False, multi_level_index=False)
        for yf_sym in INSTRUMENT_SPECS[symbol]["yf"]:
            df = self._dl(yf_sym)
            if df is not None and len(df):
                out = []
                for ts, r in df.tail(n).iterrows():
                    t = ts.to_pydatetime().astimezone(SAST)
                    out.append(Bar(t, float(r["Open"]), float(r["High"]), float(r["Low"]), float(r["Close"])))
                return out
        raise DataUnavailable(f"yfinance returned nothing for {symbol}")


class ReplayProvider:
    """Reads ``<dir>/<SYMBOL>_1m_<date>.csv`` (open-time SAST, OHLC). Never touches the network."""
    is_fallback = False

    def __init__(self, directory: str, day: str = "2026-10-14", name: str = "REPLAY:TV:OANDA"):
        self.dir, self.day, self.name = directory, day, name
        self._cache: Dict[str, List[Bar]] = {}

    def bars_1m(self, symbol, now, n=1000):
        if symbol not in self._cache:
            path = os.path.join(self.dir, f"{symbol}_1m_{self.day}.csv")
            if not os.path.exists(path):
                raise DataUnavailable(path)
            with open(path) as f:
                self._cache[symbol] = [Bar(datetime.fromisoformat(r["datetime"]).replace(tzinfo=SAST), float(r["open"]),
                                           float(r["high"]), float(r["low"]), float(r["close"])) for r in csv.DictReader(f)]
        return [b for b in self._cache[symbol] if b.time < now][-n:]


@dataclass
class Snapshot:
    as_of: datetime                       # close time of the last closed 1m bar (cycle reference)
    data_source: str
    fallback_used: bool
    bars: Dict[str, Dict[str, List[Bar]]]  # symbol -> tf -> bars
    last_closed_bar: Dict[str, Dict[str, str]] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def bars_1m(self) -> Dict[str, List[Bar]]:
        return {s: v["1m"] for s, v in self.bars.items()}

    def digest(self) -> str:
        return hashlib.sha256(json.dumps(self.last_closed_bar, sort_keys=True).encode()).hexdigest()[:16]

    def compact(self, symbol: str, tf: str, n: int = 40) -> List[list]:
        return [[b.time.isoformat(), b.open, b.high, b.low, b.close] for b in self.bars.get(symbol, {}).get(tf, [])[-n:]]


class DataService:
    TFS = ("1m", "5m", "15m", "1H", "4H", "D")

    def __init__(self, providers: List[Provider], symbols=INSTRUMENTS, cache_writer=None):
        self.providers = providers
        self.symbols = symbols
        self.cache_writer = cache_writer   # e.g. S3 put of the snapshot JSON (full) / local file (light)
        self._snap: Optional[Snapshot] = None
        self._key: Optional[datetime] = None

    def snapshot(self, now: datetime) -> Snapshot:
        """One fetch per cycle (keyed by the minute); later calls in the same cycle return the cache."""
        key = now.replace(second=0, microsecond=0)
        if self._snap is not None and self._key == key:
            return self._snap
        bars, sources, fallback, errors = {}, set(), False, []
        for sym in self.symbols:
            got = None
            for p in self.providers:
                try:
                    got = closed_only(p.bars_1m(sym, now, 1000), now)
                    if not got:
                        raise DataUnavailable("no closed bars")
                    sources.add(p.name); fallback |= p.is_fallback
                    break
                except Exception as e:  # provider down -> next provider
                    errors.append(f"{p.name}:{sym}:{type(e).__name__}:{e}"[:200])
                    log.warning("provider %s failed for %s: %s", p.name, sym, e)
            if got is None:
                continue
            bars[sym] = {"1m": got}
            for tf in self.TFS[1:]:
                bars[sym][tf] = [b for b in resample(got, tf) if b.is_closed(now)]
        if not bars:
            raise DataUnavailable("; ".join(errors))
        as_of = max(b["1m"][-1].close_time for b in bars.values())
        lcb = {s: {tf: v[tf][-1].time.isoformat() for tf in v if v[tf]} for s, v in bars.items()}
        snap = Snapshot(as_of=as_of, data_source="+".join(sorted(sources)), fallback_used=fallback, bars=bars,
                        last_closed_bar=lcb, errors=errors)
        if self.cache_writer:
            try:
                self.cache_writer(snap)
            except Exception as e:  # cache failure never breaks the cycle
                log.warning("snapshot cache write failed: %s", e)
        self._snap, self._key = snap, key
        return snap


def s3_cache_writer(bucket: str, s3=None):
    import boto3
    s3 = s3 or boto3.client("s3")

    def _w(snap: Snapshot):
        body = {"as_of": snap.as_of.isoformat(), "data_source": snap.data_source, "fallback_used": snap.fallback_used,
                "last_closed_bar": snap.last_closed_bar,
                "bars": {s: {tf: [[b.time.isoformat(), b.open, b.high, b.low, b.close] for b in v]
                             for tf, v in tfs.items()} for s, tfs in snap.bars.items()}}
        s3.put_object(Bucket=bucket, Key=f"snapshots/{snap.as_of:%Y-%m-%d}/{snap.as_of:%H%M}.json",
                      Body=json.dumps(body).encode())
    return _w
