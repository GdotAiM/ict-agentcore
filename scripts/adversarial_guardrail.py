"""Live Bedrock ApplyGuardrail adversarial suite. Requires GUARDRAIL_ID/VERSION and AWS creds.

    python scripts/adversarial_guardrail.py
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from dotenv import load_dotenv; load_dotenv()
import boto3
from ict_pipeline import config
from scripts.adversarial_checks import CASES

def main():
    gid, gver = os.environ["GUARDRAIL_ID"], os.environ["GUARDRAIL_VERSION"]
    c = boto3.client("bedrock-runtime", region_name=config.AWS_REGION)
    for name, text in CASES:
        r = c.apply_guardrail(guardrailIdentifier=gid, guardrailVersion=gver,
                              source="INPUT", content=[{"text": {"text": text}}])
        action = r.get("action")
        print(f"{name}: action={action}")
    print("done")

if __name__ == "__main__":
    main()
