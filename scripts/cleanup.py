"""Dry-run / delete ICT AgentCore resources (mirrors NovaMart cleanup)."""
import argparse, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from dotenv import load_dotenv; load_dotenv()
import boto3
from ict_pipeline import config

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--yes", action="store_true"); a = ap.parse_args()
    cf = boto3.client("cloudformation", region_name=config.AWS_REGION)
    stack = config.PROJECT_NAME
    print(f"Would delete CloudFormation stack {stack}, AgentCore runtime, KBs, guardrail, Cognito frontend.")
    print("Order: disable EventBridge schedules -> delete AgentCore runtime -> delete KBs -> "
          "python scripts/create_cognito_frontend.py --delete -> delete stack.")
    if not a.yes:
        print("Dry run. Pass --yes to delete the CloudFormation stack.")
        return
    cf.delete_stack(StackName=stack)
    print("delete_stack initiated")

if __name__ == "__main__":
    main()
