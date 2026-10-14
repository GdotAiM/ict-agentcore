"""Strands Agent builders (full AWS path). Offline tests use MockLLM instead."""
from __future__ import annotations

import os
from typing import Optional

from ..config import ORCHESTRATOR_MODEL_ID, WORKER_MODEL_ID, AWS_REGION
from ..guardrails import UNTRUSTED_RULE, guarded_content

MARKET_READ = ("bias", "timeframe", "intermarket", "liquidity", "orderflow")
FINDERS = ("entry_model", "scalp", "pingpong")
CHECKS = ("confluence", "probability", "mentor")


def _bedrock_model(model_id: str, guardrail_id: str = "", guardrail_version: str = ""):
    from strands.models import BedrockModel
    kw = {"model_id": model_id, "region_name": AWS_REGION}
    if guardrail_id and guardrail_version:
        kw["guardrail_id"] = guardrail_id
        kw["guardrail_version"] = guardrail_version
    return BedrockModel(**kw)


def build_worker(name: str, system: str, tools=None, guardrail_id: str = "", guardrail_version: str = ""):
    from strands import Agent
    return Agent(name=name, system_prompt=f"{UNTRUSTED_RULE}\n\n{system}",
                 model=_bedrock_model(WORKER_MODEL_ID, guardrail_id, guardrail_version),
                 tools=tools or [], callback_handler=None)


def build_orchestrator_agent(guardrail_id: str = "", guardrail_version: str = ""):
    from strands import Agent
    return Agent(name="orchestrator",
                 system_prompt=f"{UNTRUSTED_RULE}\nYou are the lead orchestrator. You decide cycle timing, "
                               f"fan out market-read and setup finders, collect JSON, and never invent prices.",
                 model=_bedrock_model(ORCHESTRATOR_MODEL_ID, guardrail_id, guardrail_version))


def kb_retriever(kb_id: str):
    """Bedrock Knowledge Base retrieve tool (Titan v2 / S3 Vectors)."""
    if not kb_id:
        return None
    import boto3
    client = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

    def retrieve(query: str, n: int = 5) -> list:
        r = client.retrieve(knowledgeBaseId=kb_id, retrievalQuery={"text": query},
                            retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": n}})
        return [{"text": x["content"]["text"], "score": x.get("score"),
                 "uri": (x.get("location") or {}).get("s3Location", {}).get("uri", "")}
                for x in r.get("retrievalResults", [])]
    return retrieve


def with_guard_content(agent, prompt: str, user_text: Optional[str]):
    """Invoke a Strands agent with guardContent tagging of the owner's raw text."""
    # Strands BedrockModel accepts list content blocks for Converse.
    return agent(guarded_content(prompt, user_text))
