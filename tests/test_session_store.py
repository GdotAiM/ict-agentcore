"""moto tests: custom Strands SessionRepository on DynamoDB, persisted across invokes."""
import os
import boto3
import pytest
from moto import mock_aws

os.environ["AGENT_SESSIONS_TABLE"] = "ut-agent-sessions"

from strands.session import SessionRepository
from strands.types.exceptions import SessionException
from strands.types.session import Session, SessionMessage, SessionType

from ict_pipeline import sessions as S


@pytest.fixture(scope="module", autouse=True)
def table():
    with mock_aws():
        ddb = boto3.resource("dynamodb", region_name="us-east-1")
        S.create_sessions_table(ddb, "ut-agent-sessions")
        yield ddb


def repo():
    return S.DynamoDBSessionRepository(resource=boto3.resource("dynamodb", region_name="us-east-1"))


def test_is_strands_repository():
    assert isinstance(repo(), SessionRepository)


def test_session_crud_duplicate():
    r = repo()
    r.create_session(Session(session_id="s1", session_type=SessionType.AGENT))
    assert r.read_session("s1").session_id == "s1"
    with pytest.raises(SessionException):
        r.create_session(Session(session_id="s1", session_type=SessionType.AGENT))


def test_messages_ordered_paginated():
    r = repo()
    for i in (2, 0, 11, 1):
        r.create_message("m", "a", SessionMessage(message={"role": "user", "content": [{"text": f"m{i}"}]}, message_id=i))
    assert [m.message_id for m in r.list_messages("m", "a")] == [0, 1, 2, 11]
    assert [m.message_id for m in r.list_messages("m", "a", limit=2, offset=1)] == [1, 2]


def test_history_persists_across_invokes():
    assert S.save_session_turn("own-1", "Why was S26 blocked?", "S26 was blocked: OPPOSITE_OPEN vs B14.")
    assert S.save_session_turn("own-1", "And S25?", "S25 stopped -1R at 14:59.")
    agent = S.conversation_agent("own-1")      # new process / new invoke
    texts = [c["text"] for m in agent.messages for c in m["content"]]
    assert texts[0] == "Why was S26 blocked?" and len(texts) == 4
    h = S.load_session_history("own-1")
    assert "Owner: Why was S26 blocked?" in h and "Mentor: S25 stopped" in h
    assert "S26" not in S.load_session_history("other")


def test_disabled_never_raises(monkeypatch):
    monkeypatch.setenv("AGENT_SESSIONS_ENABLED", "false")
    assert S.save_session_turn("x", "a", "b") is False and S.load_session_history("x") == ""
    monkeypatch.setenv("AGENT_SESSIONS_ENABLED", "true")
    monkeypatch.setenv("AGENT_SESSIONS_TABLE", "missing")
    assert S.save_session_turn("x", "a", "b") is False
