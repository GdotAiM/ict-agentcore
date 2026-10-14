"""AgentCore Memory (SESSION_SUMMARY) helpers + EMF/X-Ray/run-log observability, offline."""
import json
from ict_pipeline import memory as mem
from ict_pipeline.observability import RunLog, TokenBudget, XRayTracer, emf


class FakeMem:
    def __init__(self):
        self.events = []
    def list_events(self, **kw):
        return {"events": [{"eventTimestamp": "1", "payload": [{"conversational": {"role": "USER", "content": {"text": "why S26?"}}}]}]}
    def list_memory_records(self, **kw):
        assert kw["namespace"] == "/summaries/ntloso/"
        return {"memoryRecordSummaries": [{"namespaces": ["/summaries/ntloso/old"], "content": {"text": "Earlier: B14 short open."}}]}
    def create_event(self, **kw):
        self.events.append(kw); return {}


def test_memory_roundtrip(monkeypatch):
    monkeypatch.setenv("AGENTCORE_MEMORY_ID", "mem-1")
    c = FakeMem()
    ctx = mem.load_memory_context(c, "s1", "ntloso")
    assert "Earlier: B14 short open." in ctx and "Owner: why S26?" in ctx
    assert mem.save_memory_turn(c, "s1", "ntloso", "q", "a") and c.events[0]["actorId"] == "ntloso"


def test_memory_disabled(monkeypatch):
    monkeypatch.delenv("AGENTCORE_MEMORY_ID", raising=False)
    assert mem.load_memory_context(FakeMem(), "s", "o") == "" and not mem.save_memory_turn(FakeMem(), "s", "o", "q", "a")


def test_emf_shape():
    doc = json.loads(emf({"AgentLatencyMs": 12.0, "AgentInvocations": 1}, {"Agent": "bias"}))
    m = doc["_aws"]["CloudWatchMetrics"][0]
    assert m["Namespace"] == "ICT/Pipeline" and m["Dimensions"] == [["Agent"]]
    assert {"Name": "AgentLatencyMs", "Unit": "Milliseconds"} in m["Metrics"]


def test_xray_segments_published():
    sent = {}
    class C:
        def put_trace_segments(self, TraceSegmentDocuments):
            sent["docs"] = TraceSegmentDocuments
    t = XRayTracer(enabled=True, client=C())
    with t.subsegment("bias"):
        pass
    t.publish("run-1")
    doc = json.loads(sent["docs"][0])
    assert doc["annotations"]["run_id"] == "run-1" and doc["subsegments"][0]["name"] == "bias"


def test_runlog_why(tmp_path):
    log = RunLog("r1", str(tmp_path))
    log.decision("S26", False, "OPPOSITE_OPEN", "B14 short open")
    assert log.why("S26")[0]["reason"] == "OPPOSITE_OPEN"
    assert (tmp_path / "r1.jsonl").exists() is False and log.flush().endswith("r1.jsonl")


def test_budget_ddb(ddb):
    t = ddb.create_table(TableName="ops", BillingMode="PAY_PER_REQUEST",
                         KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}, {"AttributeName": "sk", "KeyType": "RANGE"}],
                         AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}, {"AttributeName": "sk", "AttributeType": "S"}])
    b = TokenBudget(100, 0.9, table=t, day="2026-10-14")
    b.add(50); assert not b.degraded(); b.add(40); assert b.degraded() and b.used() == 90
