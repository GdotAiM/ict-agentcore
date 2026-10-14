"""Create / update the Bedrock Guardrail (PROMPT_ATTACK + denied topics + PII). Writes GUARDRAIL_ID/VERSION to .env."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import boto3
from dotenv import load_dotenv; load_dotenv()
from ict_pipeline.guardrails import GUARDRAIL_SPEC
from ict_pipeline import config

NAME = GUARDRAIL_SPEC["name"]
bedrock = boto3.client("bedrock", region_name=config.AWS_REGION)
existing = {g["name"]: g for p in bedrock.get_paginator("list_guardrails").paginate() for g in p["guardrails"]}
body = {k: v for k, v in GUARDRAIL_SPEC.items() if k != "name"}
if NAME in existing:
    gid = existing[NAME]["id"]
    bedrock.update_guardrail(guardrailIdentifier=gid, name=NAME, **body)
    print(f"updated {NAME} ({gid})")
else:
    gid = bedrock.create_guardrail(name=NAME, **body)["guardrailId"]
    print(f"created {NAME} ({gid})")
ver = bedrock.create_guardrail_version(guardrailIdentifier=gid, description="analysis-only")["version"]
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
lines = open(env_path).read().splitlines() if os.path.exists(env_path) else []
kv = {l.split("=", 1)[0]: l for l in lines if "=" in l}
kv["GUARDRAIL_ID"] = f"GUARDRAIL_ID={gid}"
kv["GUARDRAIL_VERSION"] = f"GUARDRAIL_VERSION={ver}"
with open(env_path, "w") as f:
    f.write("\n".join(kv.values()) + "\n")
print(f"GUARDRAIL_ID={gid} GUARDRAIL_VERSION={ver}")
