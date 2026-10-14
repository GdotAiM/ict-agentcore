"""Create the 3 ICT Knowledge Bases on the stack's S3 Vectors store (Titan Embed Text v2, 1024-d).

Run after the stack is deployed and docs are seeded:
  python scripts/seed_kb_docs.py
  python scripts/create_knowledge_bases.py

Writes RULES_KB_ID / TRANSCRIPTS_KB_ID / BACKTESTS_KB_ID into .env.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import boto3, ict_pipeline.config as config
from dotenv import load_dotenv; load_dotenv()

agent = boto3.client("bedrock-agent", region_name=config.AWS_REGION)
role = config.resource("AgentCoreRoleArn", "AGENTCORE_ROLE_ARN")
bucket = config.resource("KbBucket", "KB_BUCKET")
vb_arn = config.resource("VectorBucketArn", "VECTOR_BUCKET_ARN")
EMB = f"arn:aws:bedrock:{config.AWS_REGION}::foundation-model/amazon.titan-embed-text-v2:0"
specs = [
    ("RULES_KB_ID", "ict-rules-kb", "rules/", "rules-index-v2"),
    ("TRANSCRIPTS_KB_ID", "ict-transcripts-kb", "transcripts/", "transcripts-index-v2"),
    ("BACKTESTS_KB_ID", "ict-backtests-kb", "backtests/", "backtests-index-v2"),
]
existing = {k["name"]: k["knowledgeBaseId"] for p in agent.get_paginator("list_knowledge_bases").paginate()
            for k in p["knowledgeBaseSummaries"]}
ids = {}
for env_key, name, prefix, index in specs:
    if name in existing:
        kb_id = existing[name]; print(f"{name}: already exists ({kb_id})")
    else:
        kb = agent.create_knowledge_base(
            name=name, roleArn=role, description=f"ICT {prefix}",
            knowledgeBaseConfiguration={"type": "VECTOR", "vectorKnowledgeBaseConfiguration": {
                "embeddingModelArn": EMB,
                "embeddingModelConfiguration": {"bedrockEmbeddingModelConfiguration": {
                    "dimensions": 1024, "embeddingDataType": "FLOAT32"}}}},
            storageConfiguration={"type": "S3_VECTORS", "s3VectorsConfiguration": {
                "vectorBucketArn": vb_arn, "indexName": index}})["knowledgeBase"]
        kb_id = kb["knowledgeBaseId"]; print(f"{name}: created {kb_id}")
    while True:
        st = agent.get_knowledge_base(knowledgeBaseId=kb_id)["knowledgeBase"]["status"]
        if st != "CREATING": break
        time.sleep(5)
    dss = agent.list_data_sources(knowledgeBaseId=kb_id)["dataSourceSummaries"]
    if dss:
        ds_id = dss[0]["dataSourceId"]
    else:
        ds_id = agent.create_data_source(
            knowledgeBaseId=kb_id, name=f"{name}-s3",
            dataSourceConfiguration={"type": "S3", "s3Configuration": {
                "bucketArn": f"arn:aws:s3:::{bucket}", "inclusionPrefixes": [prefix]}})["dataSource"]["dataSourceId"]
    ids[env_key] = (kb_id, ds_id, name)

print("\nSyncing...")
jobs = {k: agent.start_ingestion_job(knowledgeBaseId=v[0], dataSourceId=v[1])["ingestionJob"]["ingestionJobId"]
        for k, v in ids.items()}
for k, (kb_id, ds_id, name) in ids.items():
    while True:
        j = agent.get_ingestion_job(knowledgeBaseId=kb_id, dataSourceId=ds_id, ingestionJobId=jobs[k])["ingestionJob"]
        if j["status"] in ("COMPLETE", "FAILED", "STOPPED"): break
        time.sleep(5)
    print(f"  {name}: {j['status']} ({kb_id})")

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
lines = open(env_path).read().splitlines() if os.path.exists(env_path) else []
keys = {k.split("=", 1)[0] for k in lines if "=" in k}
with open(env_path, "a") as f:
    for env_key, (kb_id, _, _) in ids.items():
        if env_key not in keys:
            f.write(f"\n{env_key}={kb_id}")
print("Wrote KB IDs to .env")
