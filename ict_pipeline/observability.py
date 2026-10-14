"""Observability (SPEC section 8, NovaMart pattern): run_id, JSONL agent-call log, EMF custom
metrics, X-Ray segments (put_trace_segments), reason codes, daily token budget with degradation."""
from __future__ import annotations

import hashlib
import json
import logging
import os
import secrets
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Dict, List, Optional

log = logging.getLogger("ict.obs")
METRIC_NS = os.environ.get("METRIC_NAMESPACE", "ICT/Pipeline")


def new_run_id() -> str:
    return str(uuid.uuid4())


def input_hash(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def emf(metrics: Dict[str, float], dims: Dict[str, str], unit: str = "None") -> str:
    """CloudWatch Embedded Metric Format line (stdout of the AgentCore runtime lands in CloudWatch Logs)."""
    doc = {"_aws": {"Timestamp": int(time.time() * 1000), "CloudWatchMetrics": [{
        "Namespace": METRIC_NS, "Dimensions": [list(dims.keys())],
        "Metrics": [{"Name": k, "Unit": "Milliseconds" if k.endswith("LatencyMs") else unit} for k in metrics]}]}}
    doc.update(dims); doc.update(metrics)
    line = json.dumps(doc)
    if os.environ.get("EMF_STDOUT", "true").lower() == "true":
        print(line, flush=True)
    return line


class RunLog:
    """Per-cycle JSONL log: every agent call (input hash, output, latency, tokens, validation) and
    every rule decision with reason code, so the owner can ask 'why was X blocked'."""

    def __init__(self, run_id: str, log_dir: str = "out/logs"):
        self.run_id = run_id
        self.records: List[dict] = []
        self.dir = log_dir
        self._lock = threading.Lock()

    def add(self, kind: str, **kw):
        rec = {"run_id": self.run_id, "kind": kind, "ts": datetime.now(timezone.utc).isoformat(), **kw}
        with self._lock:
            self.records.append(rec)
        return rec

    def agent_call(self, agent: str, inp, output, latency_ms: float, tokens: int, valid: bool, error: str = ""):
        self.add("agent_call", agent=agent, input_hash=input_hash(inp), output=output, latency_ms=round(latency_ms, 1),
                 tokens=tokens, valid=valid, error=error)
        emf({"AgentInvocations": 1, "AgentLatencyMs": latency_ms, "AgentTokens": tokens, "AgentInvalidOutput": 0 if valid else 1},
            {"Agent": agent})

    def decision(self, candidate_id: str, passed: bool, reason: Optional[str], detail: str = ""):
        self.add("rule_decision", candidate_id=candidate_id, passed=passed, reason=reason, detail=detail)
        emf({"RuleBlocked": 0 if passed else 1, "RulePassed": 1 if passed else 0}, {"Reason": reason or "PASS"})

    def flush(self) -> str:
        os.makedirs(self.dir, exist_ok=True)
        path = os.path.join(self.dir, f"{self.run_id}.jsonl")
        with open(path, "w") as f:
            for r in self.records:
                f.write(json.dumps(r, default=str) + "\n")
        return path

    def why(self, candidate_id: str) -> List[dict]:
        return [r for r in self.records if r.get("candidate_id") == candidate_id]


class TokenBudget:
    """Daily token budget. Backed by the ops DynamoDB table (atomic ADD) or in-memory for light/test."""

    def __init__(self, limit: int, degrade_at: float = 0.9, table=None, day: Optional[str] = None):
        self.limit, self.degrade_at, self.table = limit, degrade_at, table
        self.day = day or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._mem = 0

    def used(self) -> int:
        if self.table is None:
            return self._mem
        it = self.table.get_item(Key={"pk": f"BUDGET#{self.day}", "sk": "tokens"}).get("Item")
        return int(it["used"]) if it else 0

    def add(self, tokens: int):
        if self.table is None:
            self._mem += int(tokens); return
        self.table.update_item(Key={"pk": f"BUDGET#{self.day}", "sk": "tokens"},
                               UpdateExpression="ADD used :t", ExpressionAttributeValues={":t": int(tokens)})

    def degraded(self) -> bool:
        return self.used() >= self.limit * self.degrade_at


class XRayTracer:
    """Minimal X-Ray publisher (same approach as NovaMart agent_observability): one segment per run,
    one subsegment per agent; published with PutTraceSegments when AGENT_TRACING_ENABLED=true."""

    def __init__(self, enabled: Optional[bool] = None, client=None):
        self.enabled = (os.environ.get("AGENT_TRACING_ENABLED", "false").lower() == "true") if enabled is None else enabled
        self._client = client
        self.trace_id = f"1-{int(time.time()):08x}-{secrets.token_hex(12)}"
        self.root = {"name": "ict-orchestrator", "id": secrets.token_hex(8), "trace_id": self.trace_id,
                     "start_time": time.time(), "subsegments": [], "annotations": {}}
        self._lock = threading.Lock()

    @contextmanager
    def subsegment(self, name: str, **annotations):
        seg = {"name": name, "id": secrets.token_hex(8), "start_time": time.time(), "annotations": annotations}
        try:
            yield seg
        except Exception as e:
            seg["fault"] = True; seg["cause"] = {"exceptions": [{"message": str(e)[:200]}]}
            raise
        finally:
            seg["end_time"] = time.time()
            with self._lock:
                self.root["subsegments"].append(seg)

    def publish(self, run_id: str) -> Optional[str]:
        self.root["end_time"] = time.time()
        self.root["annotations"]["run_id"] = run_id
        if not self.enabled:
            return None
        try:
            import boto3
            c = self._client or boto3.client("xray")
            c.put_trace_segments(TraceSegmentDocuments=[json.dumps(self.root)])
        except Exception as e:  # tracing never breaks a cycle
            log.warning("xray publish failed: %s", e)
        return self.trace_id
