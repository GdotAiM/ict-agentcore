"""AgentCore Memory helpers (SESSION_SUMMARY long-term + short-term conversational events).

Mirrors NovaMart: never raises into a request; Memory is complementary to the DynamoDB SessionRepository.
Actor id = owner name (config), session id = run/session id.
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

log = logging.getLogger("ict.memory")
_MAX_TURNS, _MAX_CHARS = 6, 4000


def memory_id() -> Optional[str]:
    if os.environ.get("AGENT_MEMORY_ENABLED", "true").strip().lower() in ("0", "false", "no"):
        return None
    return (os.environ.get("AGENTCORE_MEMORY_ID") or "").strip() or None


def load_memory_context(client, session_id: str, owner_id: str) -> str:
    mid = memory_id()
    if not mid or not owner_id or client is None:
        return ""
    lines, summaries = [], []
    try:
        resp = client.list_events(memoryId=mid, actorId=owner_id, sessionId=session_id,
                                  includePayloads=True, maxResults=_MAX_TURNS * 2)
        for ev in sorted(resp.get("events", []), key=lambda e: str(e.get("eventTimestamp", ""))):
            for item in ev.get("payload", []):
                conv = item.get("conversational") or {}
                text = (conv.get("content") or {}).get("text", "").strip()
                if text:
                    who = "Owner" if conv.get("role") == "USER" else "Pipeline"
                    lines.append(f"{who}: {text[:1200]}")
    except Exception as e:
        log.warning("AgentCore Memory list_events failed: %s", e)
    try:
        resp = client.list_memory_records(memoryId=mid, namespace=f"/summaries/{owner_id}/", maxResults=10)
        for rec in resp.get("memoryRecordSummaries", []):
            if any(ns.rstrip("/").endswith("/" + session_id) for ns in rec.get("namespaces", [])):
                continue
            text = ((rec.get("content") or {}).get("text") or "").strip()
            if text:
                summaries.append(text[:800])
    except Exception as e:
        log.warning("AgentCore Memory list_memory_records failed: %s", e)
    parts = []
    if summaries:
        parts.append("Summaries of earlier sessions:\n- " + "\n- ".join(summaries[:3]))
    if lines:
        parts.append("Earlier turns in this conversation:\n" + "\n".join(lines))
    return "\n\n".join(parts)[-_MAX_CHARS:]


def save_memory_turn(client, session_id: str, owner_id: str, user_text: str, assistant_text: str) -> bool:
    mid = memory_id()
    if not mid or not owner_id or client is None:
        return False
    payload = [{"conversational": {"role": "USER", "content": {"text": (user_text or "")[:8000]}}}]
    if assistant_text:
        payload.append({"conversational": {"role": "ASSISTANT", "content": {"text": assistant_text[:8000]}}})
    try:
        client.create_event(memoryId=mid, actorId=owner_id, sessionId=session_id,
                            eventTimestamp=datetime.now(timezone.utc), payload=payload, clientToken=str(uuid.uuid4()))
        return True
    except Exception as e:
        log.warning("AgentCore Memory create_event failed: %s", e)
        return False
