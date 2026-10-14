"""Pluggable notifier. Default writes the combined call to a local file/log. Telegram/email are
STUBS: they build the payload and log it but never open a network connection (dry run only).
Turning them into real senders is a deliberate owner decision outside this repo."""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Protocol

log = logging.getLogger("ict.notify")


class Notifier(Protocol):
    def send(self, text: str, call: dict) -> dict: ...


class FileNotifier:
    def __init__(self, directory: str = "out/alerts"):
        self.dir = directory

    def send(self, text, call):
        os.makedirs(self.dir, exist_ok=True)
        path = os.path.join(self.dir, f"{call.get('run_id', 'run')}.md")
        with open(path, "w") as f:
            f.write(text)
        with open(os.path.join(self.dir, "calls.jsonl"), "a") as f:
            f.write(json.dumps(call, default=str) + "\n")
        log.info("alert written to %s", path)
        return {"channel": "file", "path": path, "sent": False}


class TelegramStub:
    """Configured by TELEGRAM_CHAT_ID (and a bot token kept OUT of the repo). Dry-run only."""

    def __init__(self, chat_id: str = ""):
        self.chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID", "")

    def send(self, text, call):
        payload = {"chat_id": self.chat_id, "text": text[:4000]}
        log.info("TELEGRAM DRY-RUN (not sent): %s", json.dumps(payload)[:300])
        return {"channel": "telegram", "dry_run": True, "sent": False, "payload": payload}


class EmailStub:
    """Configured by ALERT_EMAIL_TO / ALERT_EMAIL_FROM (SES in AWS). Dry-run only."""

    def __init__(self, to: str = "", sender: str = ""):
        self.to = to or os.environ.get("ALERT_EMAIL_TO", "")
        self.sender = sender or os.environ.get("ALERT_EMAIL_FROM", "")

    def send(self, text, call):
        msg = {"to": self.to, "from": self.sender, "subject": f"ICT call {call.get('kill_zone')} {call.get('headline')}", "body": text}
        log.info("EMAIL DRY-RUN (not sent): %s", msg["subject"])
        return {"channel": "email", "dry_run": True, "sent": False, "payload": msg}


class NullNotifier:
    """Replay mode: nothing leaves the process."""
    def __init__(self):
        self.outbox = []

    def send(self, text, call):
        self.outbox.append(text)
        return {"channel": "null", "sent": False}


def build(channel: str, alert_dir: str = "out/alerts") -> Notifier:
    return {"telegram": TelegramStub, "email": EmailStub}.get(channel, lambda: FileNotifier(alert_dir))() \
        if channel in ("telegram", "email") else FileNotifier(alert_dir)
