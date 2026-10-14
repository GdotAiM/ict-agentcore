"""Create AgentCore Memory with the SESSION_SUMMARY (summaryMemoryStrategy) strategy, 7-day events.
Writes AGENTCORE_MEMORY_ID to .env."""
import os, sys, time, uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv; load_dotenv()
import boto3
from ict_pipeline import config

NAME = os.environ.get("MEMORY_NAME", config.PROJECT_NAME.replace("-", "_") + "_memory")
ctl = boto3.client("bedrock-agentcore-control", region_name=config.AWS_REGION)
existing = [m for m in ctl.list_memories().get("memories", []) if m.get("id", "").startswith(NAME)]
if existing:
    mid = existing[0]["id"]; print("memory exists", mid)
else:
    mid = ctl.create_memory(
        name=NAME, description="ICT owner session summaries (7-day event retention)", eventExpiryDuration=7,
        memoryStrategies=[{"summaryMemoryStrategy": {"name": "SessionSummary",
                                                     "namespaces": ["/summaries/{actorId}/{sessionId}"]}}],
        clientToken=str(uuid.uuid4()))["memory"]["id"]
    print("created", mid)
    while ctl.get_memory(memoryId=mid)["memory"]["status"] == "CREATING":
        time.sleep(5)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
lines = open(env_path).read().splitlines() if os.path.exists(env_path) else []
lines = [l for l in lines if not l.startswith("AGENTCORE_MEMORY_ID=")] + [f"AGENTCORE_MEMORY_ID={mid}"]
open(env_path, "w").write("\n".join(lines) + "\n")
print("AGENTCORE_MEMORY_ID", mid)
