"""Single trade-state table (SPEC section 5) on DynamoDB.

* One item per trade_id. Single writer: only the orchestrator/rule engine holds a ``TradeStateWriter``.
* Every change is a conditional write with optimistic locking (``expected_version``), the NovaMart
  WorkflowState pattern; creation uses ``attribute_not_exists(trade_id)``.
* ``history`` is append-only (list_append) with who/when.
* Agents and humans read through ``TradeStateReader`` and never declare fills.
"""
from __future__ import annotations

import json
import time
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from botocore.exceptions import ClientError

STATUSES = ("proposed", "pending", "filled", "closed", "cancelled", "expired", "blocked")
TRANSITIONS = {
    "proposed": {"pending", "blocked", "cancelled"},
    "pending": {"filled", "cancelled", "expired"},
    "filled": {"closed"},
}
WRITER_ID = "rule_engine"


class VersionConflict(RuntimeError):
    pass


class IllegalTransition(ValueError):
    pass


def _to_ddb(v):
    if isinstance(v, float):
        return Decimal(str(v))
    if isinstance(v, dict):
        return {k: _to_ddb(x) for k, x in v.items() if x is not None}
    if isinstance(v, list):
        return [_to_ddb(x) for x in v]
    return v


def _from_ddb(v):
    if isinstance(v, Decimal):
        return int(v) if v == v.to_integral_value() and "." not in str(v) else float(v)
    if isinstance(v, dict):
        return {k: _from_ddb(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_from_ddb(x) for x in v]
    return v


class TradeStateReader:
    def __init__(self, table_name: str, resource=None, region: str = "us-east-1"):
        import boto3
        self.table = (resource or boto3.resource("dynamodb", region_name=region)).Table(table_name)

    def get(self, trade_id: str) -> Optional[dict]:
        item = self.table.get_item(Key={"trade_id": trade_id}, ConsistentRead=True).get("Item")
        return _from_ddb(item) if item else None

    def all(self) -> List[dict]:
        items, kw = [], {"ConsistentRead": True}
        while True:
            r = self.table.scan(**kw)
            items += r.get("Items", [])
            if "LastEvaluatedKey" not in r:
                break
            kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
        return sorted((_from_ddb(i) for i in items), key=lambda t: t.get("created_at", ""))

    def active(self) -> List[dict]:
        return [t for t in self.all() if t.get("status") in ("pending", "filled")]


class TradeStateWriter(TradeStateReader):
    """The ONLY writer. Construct once per cycle inside the orchestrator."""

    def __init__(self, table_name: str, resource=None, region: str = "us-east-1", writer: str = WRITER_ID):
        if writer != WRITER_ID:
            raise PermissionError("trade-state has a single writer (rule_engine)")
        super().__init__(table_name, resource, region)
        self.writer = writer

    def create(self, trade: dict, at: datetime, status: str = "pending") -> dict:
        item = dict(trade)
        item.update(status=status, version=0, created_at=at.isoformat(), last_writer=self.writer,
                    history=[{"status": status, "at": at.isoformat(), "by": self.writer, "note": "created"}])
        try:
            self.table.put_item(Item=_to_ddb(item), ConditionExpression="attribute_not_exists(trade_id)")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise VersionConflict(f"trade {trade['trade_id']} already exists") from e
            raise
        return item

    def transition(self, trade_id: str, new_status: Optional[str], expected_version: int, at: datetime,
                   note: str = "", record_history: bool = True, **fields) -> dict:
        """Conditional update: succeeds only if stored version == expected_version."""
        cur = self.get(trade_id)
        if cur is None:
            raise KeyError(trade_id)
        if new_status and new_status != cur["status"] and new_status not in TRANSITIONS.get(cur["status"], set()):
            raise IllegalTransition(f"{trade_id}: {cur['status']} -> {new_status}")
        sets, names, vals = ["#v = :nv", "last_writer = :w"], {"#v": "version"}, {}
        vals.update({":nv": expected_version + 1, ":ev": expected_version, ":w": self.writer})
        if record_history:
            sets.append("history = list_append(history, :h)")
            vals[":h"] = [{"status": new_status or cur["status"], "at": at.isoformat(), "by": self.writer, "note": note}]
        if new_status:
            sets.append("#s = :s"); names["#s"] = "status"; vals[":s"] = new_status
        for i, (k, v) in enumerate(fields.items()):
            if v is None:
                continue
            names[f"#f{i}"] = k; vals[f":f{i}"] = v; sets.append(f"#f{i} = :f{i}")
        try:
            r = self.table.update_item(
                Key={"trade_id": trade_id}, UpdateExpression="SET " + ", ".join(sets),
                ConditionExpression="#v = :ev", ExpressionAttributeNames=names,
                ExpressionAttributeValues=_to_ddb(vals), ReturnValues="ALL_NEW")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise VersionConflict(f"{trade_id}: expected version {expected_version}") from e
            raise
        return _from_ddb(r["Attributes"])

    def transition_retry(self, trade_id: str, new_status, at, note="", retries: int = 3, record_history=True, **fields) -> dict:
        """Optimistic-lock retry loop (re-read version, re-validate, re-apply)."""
        for attempt in range(retries):
            cur = self.get(trade_id)
            try:
                return self.transition(trade_id, new_status, int(cur["version"]), at, note, record_history, **fields)
            except VersionConflict:
                time.sleep(0.05 * (attempt + 1))
        raise VersionConflict(f"{trade_id}: gave up after {retries} attempts")

    def set_taken_by_owner(self, trade_id: str, taken: bool, at: datetime) -> dict:
        return self.transition_retry(trade_id, None, at, note=f"owner confirmed taken={taken}", taken_by_owner=taken)


def create_table(resource, name: str):
    """Used by tests/replay (moto) and documented in infrastructure/stack.yaml."""
    t = resource.create_table(TableName=name, BillingMode="PAY_PER_REQUEST",
                              KeySchema=[{"AttributeName": "trade_id", "KeyType": "HASH"}],
                              AttributeDefinitions=[{"AttributeName": "trade_id", "AttributeType": "S"}])
    t.wait_until_exists()
    return t


def dumps(trades: List[dict]) -> str:
    return json.dumps(trades, indent=2, default=str)
