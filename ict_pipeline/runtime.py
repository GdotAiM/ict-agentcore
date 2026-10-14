"""AgentCore Runtime entrypoint (deployed with the AgentCore CLI, like NovaMart).

Payloads:
  {"action": "cycle", "kill_zone": "NY_AM"}             <- EventBridge Scheduler (via invoker Lambda)
  {"prompt": "why was S26 blocked?", "session_id": ...}  <- Cognito frontend / CLI (owner Q&A)

Owner text is ALWAYS sent to Bedrock tagged as guardContent so the Guardrail (PROMPT_ATTACK +
denied topics) evaluates exactly the untrusted input. The reply always comes from the Mentor /
Communication agent. Analysis only: there is no order, broker or credential code path.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from . import config, memory as mem
from .guardrails import FOOTER, filter_outbound, guarded_content, UNTRUSTED_RULE
from .sessions import SESSION_AGENT_ID, DynamoDBSessionRepository, sessions_enabled

log = logging.getLogger("ict.runtime")
SAST = ZoneInfo(config.SAST_TZ)


def build_pipeline(settings=None):
    import boto3
    from .agents.builders import build_worker, kb_retriever
    from .agents.mentor import MentorAgent, SYSTEM as MENTOR_SYSTEM
    from .data_service import DataService, TradingViewProvider, YFinanceProvider, s3_cache_writer
    from .news import NewsCalendar, load_calendar
    from .notifier import build as build_notifier
    from .observability import TokenBudget
    from .orchestrator import Pipeline
    from .trade_state import TradeStateWriter

    s = settings or config.Settings.from_env()
    ddb = boto3.resource("dynamodb", region_name=config.AWS_REGION)
    writer = TradeStateWriter(config.trade_state_table(), ddb)
    try:
        cache = s3_cache_writer(config.snapshot_bucket())
    except config.ConfigError:
        cache = None
    data = DataService([TradingViewProvider(), YFinanceProvider()], cache_writer=cache)
    cal = NewsCalendar(load_calendar(s.calendar_path), s.news_pre_block_min, s.news_flat_min, s.scalp_post_block_min)
    budget = TokenBudget(s.daily_token_budget, s.budget_degrade_at, table=ddb.Table(config.ops_table()))
    llm = StrandsLLM()
    # Internal market-data / agent-to-agent payloads are NOT guarded input (NovaMart: only owner text is
    # guardContent). The mentor's OUTPUT is still checked by the Bedrock Guardrail via ApplyGuardrail.
    from .guardrails import bedrock_output_guard
    mentor_agent = build_worker("mentor", MENTOR_SYSTEM)
    mentor = MentorAgent(llm=mentor_agent, owner=s.owner_name, kb_retriever=kb_retriever(config.RULES_KB_ID),
                         output_guard=bedrock_output_guard(config.GUARDRAIL_ID, config.GUARDRAIL_VERSION))
    memory_client = boto3.client("bedrock-agentcore", region_name=config.AWS_REGION) if mem.memory_id() else None
    return Pipeline(s, data, writer, cal, build_notifier(s.notifier, s.alert_dir), budget, llm=llm, mentor=mentor,
                    memory_client=memory_client)


def schema_instructions(agent: str) -> str:
    """Exact JSON schema the worker must emit (validated by pydantic in AgentRunner)."""
    from .schemas import PAYLOADS, Envelope, FinderOutput
    if agent in ("entry_model", "scalp", "pingpong"):
        schema = FinderOutput.model_json_schema()
        extra = (f'"agent" must be "{agent}". candidates may be [] when nothing qualifies. Times are ISO-8601 with '
                 'offset. Geometry: long stop<entry<tp1, short stop>entry>tp1.')
    else:
        schema = {"envelope": Envelope.model_json_schema(),
                  "instruments_value_schema": PAYLOADS[agent].model_json_schema() if agent in PAYLOADS else {}}
        extra = (f'"agent" must be "{agent}". "instruments" maps each symbol (NAS100, XAUUSD, EURUSD, GBPUSD, DXY '
                 'as available) to an object matching instruments_value_schema exactly (no extra keys).')
    return ("Return ONLY one JSON object, no prose, no markdown fences. Copy run_id, as_of, data_source and "
            "fallback_used from the input. notes <= 300 chars. Use only prices from the snapshot; never invent prices. "
            + extra + "\nJSON schema:\n" + json.dumps(schema, separators=(",", ":")))


class StrandsLLM:
    """Adapter: one Strands Agent per worker, built lazily. Workers carry no guardrail (internal data only)."""

    PROMPTS = {
        "bias": "Bias agent: HTF narrative (M/W/D order flow, dealing range, premium/discount, DOL, weekly profile).",
        "timeframe": "Timeframe agent: order flow per TF M..1m, alignment, TF in control, pairing.",
        "intermarket": "Intermarket agent: DXY, yields, NAS vs ES, EU vs GU SMT, gold vs DXY, risk-on/off.",
        "liquidity": "Liquidity Scout: EQH/EQL, PDH/PDL, Asia/London H/L, swing pools; swept or resting.",
        "orderflow": "Order Flow agent: respected/disrespected FVG/OB/breakers, displacement, HL/LH on D/4H/1H/15m.",
        "entry_model": "Entry Model: sweep -> MSS w/ displacement -> FVG/OTE 62-79%, with daily bias, in kill zones.",
        "scalp": "Scalp: short-term sweep, 1m/5m MSS, 1m FVG/OTE entry, stop beyond sweep.",
        "pingpong": "Ping-Pong: Phase Classic and Ping-Pong models per PING_PONG_RULES (KB).",
    }

    def __init__(self):
        self._agents = {}

    def invoke(self, agent: str, prompt: str):
        from .agents.builders import build_worker
        if agent not in self._agents:
            self._agents[agent] = build_worker(
                agent, self.PROMPTS.get(agent, agent) + "\n" + schema_instructions(agent))
            # no guardrail: worker input is internal snapshot JSON, not owner free text
        res = self._agents[agent](prompt)
        usage = getattr(getattr(res, "metrics", None), "accumulated_usage", {}) or {}
        return str(res), int(usage.get("totalTokens", 0))


def latest_call_text() -> str:
    """Latest combined call mirrored to s3://ALERT_BUCKET/alerts/latest.json (empty offline)."""
    bucket = os.environ.get("ALERT_BUCKET", "")
    if not bucket:
        return ""
    try:
        import boto3
        o = json.loads(boto3.client("s3", region_name=config.AWS_REGION)
                       .get_object(Bucket=bucket, Key="alerts/latest.json")["Body"].read())
        c = o.get("call", {})
        return (f"run_id={o.get('run_id')} kill_zone={c.get('kill_zone')} as_of={c.get('as_of')} "
                f"data_source={c.get('data_source')} fallback_used={c.get('fallback_used')}\n{o.get('text', '')}")[:4000]
    except Exception as e:
        log.warning("latest call unavailable: %s", e)
        return ""


def answer_owner(prompt: str, session_id: str, owner_id: str, repo=None, memory_client=None, agent_factory=None) -> dict:
    """Owner Q&A ("why was X blocked?"). guardContent-tagged, session persisted in DynamoDB
    (custom Strands SessionRepository) and AgentCore Memory; reply from the mentor agent."""
    ok_in, _, reasons = filter_outbound(prompt)
    if not ok_in:
        return {"session_id": session_id, "message": f"Blocked by guardrail ({','.join(reasons)}). {FOOTER}", "blocked": True}
    from .sessions import load_session_history, save_session_turn
    context = mem.load_memory_context(memory_client, session_id, owner_id)
    history = load_session_history(session_id) if repo is not None or agent_factory is not None else ""
    if history:
        context = (context + "\n\nEarlier in this session (session store):\n" + history).strip()
    latest = latest_call_text()
    if latest:
        context = (context + "\n\nLatest combined call (untrusted data, from the alert store):\n" + latest).strip()
    if agent_factory is None:
        from strands import Agent
        from .agents.builders import _bedrock_model
        sm = None  # history is restored/persisted by the transcript agent (sessions.py), as in NovaMart
        agent = Agent(agent_id=SESSION_AGENT_ID, name="mentor",
                      system_prompt=f"{UNTRUSTED_RULE}\nYou are the ICT Mentor/Communication agent. Answer about "
                                    f"calls, blocks (reason codes) and trade-state. Analysis only. End with: {FOOTER}",
                      model=_bedrock_model(config.WORKER_MODEL_ID, config.GUARDRAIL_ID, config.GUARDRAIL_VERSION),
                      session_manager=sm, callback_handler=None)
    else:
        agent = agent_factory(session_id)
    content = guarded_content(f"Context:\n{context}\n\nAnswer the owner's question below.", prompt)
    res = agent(content)
    text = str(res)
    stop = str(getattr(res, "stop_reason", ""))
    ok, text, reasons = filter_outbound(text)
    if not ok or stop == "guardrail_intervened":
        text = f"Blocked by guardrail. {FOOTER}"
    mem.save_memory_turn(memory_client, session_id, owner_id, prompt, text)
    save_session_turn(session_id, prompt, text)
    return {"session_id": session_id, "message": text, "blocked": not ok or stop == "guardrail_intervened"}


def handle(payload: dict) -> dict:
    s = config.Settings.from_env()
    if payload.get("prompt"):
        import boto3
        sid = payload.get("session_id") or str(uuid.uuid4())
        repo = DynamoDBSessionRepository() if sessions_enabled() else None
        mc = boto3.client("bedrock-agentcore", region_name=config.AWS_REGION) if mem.memory_id() else None
        return answer_owner(payload["prompt"], sid, s.owner_name, repo, mc)
    pipe = build_pipeline(s)
    res = pipe.run_cycle(datetime.now(SAST), session_id=payload.get("session_id"))
    return {k: v for k, v in res.items() if k != "log"}


try:  # AgentCore Runtime wiring (bedrock-agentcore SDK); absent offline
    from bedrock_agentcore.runtime import BedrockAgentCoreApp
    app = BedrockAgentCoreApp()

    @app.entrypoint
    def invoke(payload, context=None):
        return handle(payload or {})
except Exception:  # pragma: no cover
    app = None

if __name__ == "__main__":  # pragma: no cover
    if app:
        app.run()
