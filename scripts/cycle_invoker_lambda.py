"""Thin Lambda that EventBridge Scheduler calls each 5 min in a kill zone; invokes the AgentCore runtime.
Deployed by scripts/deploy.py (function name ${PROJECT_NAME}-cycle-invoker)."""
import json, os, uuid
import boto3

client = boto3.client("bedrock-agentcore")


def handler(event, context):
    sid = f"cycle-{event.get('kill_zone', 'KZ')}-{uuid.uuid4()}"[:64].ljust(33, "0")
    r = client.invoke_agent_runtime(agentRuntimeArn=os.environ["AGENTCORE_RUNTIME_ARN"], runtimeSessionId=sid,
                                    payload=json.dumps({"action": "cycle", **event}).encode())
    return {"status": r.get("statusCode"), "session": sid}
