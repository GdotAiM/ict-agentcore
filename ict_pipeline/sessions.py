"""Custom Strands SessionRepository on DynamoDB (NovaMart stand-out extra).

Complements AgentCore Memory: Memory gives per-owner SESSION_SUMMARY across sessions;
this store keeps the exact Strands message history of one session so a follow-up with the
same session id can recall earlier messages. The orchestrator still never writes the final
reply: what is stored is the owner message and the Mentor/Communication agent's final text.
"""
from __future__ import annotations

import json
import os
import time
from typing import Optional

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

try:
    from strands.session import SessionRepository as _StrandsSessionRepository
except Exception:  # pragma: no cover
    _StrandsSessionRepository = object

SESSION_AGENT_ID = "owner_conversation"


def sessions_table_name() -> str:
    return os.environ.get("AGENT_SESSIONS_TABLE") or f"{os.environ.get('PROJECT_NAME', 'ict-agentcore')}-agent-sessions"


def sessions_enabled() -> bool:
    return os.environ.get("AGENT_SESSIONS_ENABLED", "true").strip().lower() not in ("0", "false", "no")


class DynamoDBSessionRepository(_StrandsSessionRepository):
    """Keys: pk=session_id, sk='SESSION'|'AGENT#id'|'MSG#agent#msg_id'|'MULTI#id'. Payload in ``data``."""

    def __init__(self, table_name: str = None, resource=None, ttl_days: int = 30):
        import boto3
        self.table = (resource or boto3.resource("dynamodb")).Table(table_name or sessions_table_name())
        self.ttl_days = ttl_days

    def _put(self, pk, sk, data, must_not_exist=False):
        item = {"pk": pk, "sk": sk, "data": json.dumps(data, default=str),
                "ttl": int(time.time()) + self.ttl_days * 86400}
        kw = {"ConditionExpression": "attribute_not_exists(pk)"} if must_not_exist else {}
        self.table.put_item(Item=item, **kw)

    def _get(self, pk, sk):
        item = self.table.get_item(Key={"pk": pk, "sk": sk}).get("Item")
        return json.loads(item["data"]) if item else None

    def create_session(self, session, **kwargs):
        from strands.types.exceptions import SessionException
        try:
            self._put(session.session_id, "SESSION", session.to_dict(), must_not_exist=True)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise SessionException(f"Session {session.session_id} already exists") from e
            raise
        return session

    def read_session(self, session_id, **kwargs):
        from strands.types.session import Session
        data = self._get(session_id, "SESSION")
        return Session.from_dict(data) if data else None

    def create_agent(self, session_id, session_agent, **kwargs):
        self._put(session_id, f"AGENT#{session_agent.agent_id}", session_agent.to_dict())

    def read_agent(self, session_id, agent_id, **kwargs):
        from strands.types.session import SessionAgent
        data = self._get(session_id, f"AGENT#{agent_id}")
        return SessionAgent.from_dict(data) if data else None

    def update_agent(self, session_id, session_agent, **kwargs):
        from strands.types.exceptions import SessionException
        prev = self.read_agent(session_id, session_agent.agent_id)
        if prev is None:
            raise SessionException(f"Agent {session_agent.agent_id} does not exist")
        session_agent.created_at = prev.created_at
        self.create_agent(session_id, session_agent)

    def create_message(self, session_id, agent_id, session_message, **kwargs):
        self._put(session_id, f"MSG#{agent_id}#{session_message.message_id:08d}", session_message.to_dict())

    def read_message(self, session_id, agent_id, message_id, **kwargs):
        from strands.types.session import SessionMessage
        data = self._get(session_id, f"MSG#{agent_id}#{message_id:08d}")
        return SessionMessage.from_dict(data) if data else None

    def update_message(self, session_id, agent_id, session_message, **kwargs):
        from strands.types.exceptions import SessionException
        prev = self.read_message(session_id, agent_id, session_message.message_id)
        if prev is None:
            raise SessionException(f"Message {session_message.message_id} does not exist")
        session_message.created_at = prev.created_at
        self.create_message(session_id, agent_id, session_message)

    def list_messages(self, session_id, agent_id, limit=None, offset=0, **kwargs):
        from strands.types.session import SessionMessage
        items, kw = [], {"KeyConditionExpression": Key("pk").eq(session_id) & Key("sk").begins_with(f"MSG#{agent_id}#")}
        while True:
            resp = self.table.query(**kw)
            items += resp.get("Items", [])
            if "LastEvaluatedKey" not in resp:
                break
            kw["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
        items.sort(key=lambda i: i["sk"])
        items = items[offset:] if limit is None else items[offset:offset + limit]
        return [SessionMessage.from_dict(json.loads(i["data"])) for i in items]

    def create_multi_agent(self, session_id, multi_agent, **kwargs):
        self._put(session_id, f"MULTI#{multi_agent.id}", multi_agent.serialize_state())

    def read_multi_agent(self, session_id, multi_agent_id, **kwargs):
        return self._get(session_id, f"MULTI#{multi_agent_id}")

    def update_multi_agent(self, session_id, multi_agent, **kwargs):
        self.create_multi_agent(session_id, multi_agent)


def create_sessions_table(resource, name: Optional[str] = None):
    name = name or sessions_table_name()
    t = resource.create_table(
        TableName=name, BillingMode="PAY_PER_REQUEST",
        KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}, {"AttributeName": "sk", "KeyType": "RANGE"}],
        AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}, {"AttributeName": "sk", "AttributeType": "S"}])
    t.wait_until_exists()
    return t


def conversation_agent(session_id: str, repository=None, resource=None):
    """A never-invoked Strands Agent whose history is persisted by RepositorySessionManager
    (DynamoDBSessionRepository). Constructing it restores earlier messages from DynamoDB."""
    from strands import Agent
    from strands.models import BedrockModel
    from strands.session import RepositorySessionManager
    from .config import AWS_REGION, WORKER_MODEL_ID
    manager = RepositorySessionManager(session_id=session_id,
                                       session_repository=repository or DynamoDBSessionRepository(resource=resource))
    agent = Agent(agent_id=SESSION_AGENT_ID, name="SessionTranscript",
                  model=BedrockModel(model_id=WORKER_MODEL_ID, region_name=AWS_REGION),
                  session_manager=manager, callback_handler=None)
    agent._ict_session_manager = manager
    return agent


def load_session_history(session_id: str, max_turns: int = 6, resource=None) -> str:
    if not sessions_enabled():
        return ""
    try:
        agent = conversation_agent(session_id, resource=resource)
        lines = []
        for msg in agent.messages[-max_turns * 2:]:
            text = " ".join(c.get("text", "") for c in msg.get("content", []) if "text" in c).strip()
            if text:
                lines.append(f"{'Owner' if msg['role'] == 'user' else 'Mentor'}: {text[:1200]}")
        return "\n".join(lines)
    except Exception:
        return ""


def save_session_turn(session_id: str, user_text: str, assistant_text: str, resource=None) -> bool:
    """Append owner message + the Mentor agent's final reply (never orchestrator text)."""
    if not sessions_enabled():
        return False
    try:
        agent = conversation_agent(session_id, resource=resource)
        manager = agent._ict_session_manager
        for role, text in (("user", user_text), ("assistant", assistant_text)):
            if text:
                msg = {"role": role, "content": [{"text": text[:8000]}]}
                agent.messages.append(msg)
                manager.append_message(msg, agent)
        manager.sync_agent(agent)
        return True
    except Exception:
        return False
