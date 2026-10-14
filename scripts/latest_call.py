"""Print the latest combined call written by the deployed runtime (s3://ALERT_BUCKET/alerts/latest.json).
Read-only. Usage: python scripts/latest_call.py [--json] [--run-id ID]"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import boto3
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
a = argparse.ArgumentParser(); a.add_argument("--json", action="store_true"); a.add_argument("--run-id")
args = a.parse_args()
bucket = os.environ.get("ALERT_BUCKET") or os.environ["SNAPSHOT_BUCKET"]
key = f"alerts/{args.run_id}.json" if args.run_id else "alerts/latest.json"
obj = json.loads(boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))
                 .get_object(Bucket=bucket, Key=key)["Body"].read())
print(json.dumps(obj, indent=2, default=str) if args.json else f"[{obj['run_id']} @ {obj['written_at']}]\n{obj['text']}")
