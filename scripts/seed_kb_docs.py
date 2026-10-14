"""Upload rule files + backtest summaries to the KB documents bucket (no transcripts downloaded)."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
import boto3
from dotenv import load_dotenv; load_dotenv()
from ict_pipeline import config

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / "kb"
(LOCAL / "rules").mkdir(parents=True, exist_ok=True)
(LOCAL / "backtests").mkdir(parents=True, exist_ok=True)
(LOCAL / "transcripts").mkdir(parents=True, exist_ok=True)
# Copy team rules (already redacted in reference/)
for src, dst in [
    (ROOT / "reference/TEAM_PLAN.md", LOCAL / "rules/TEAM_PLAN.md"),
    (ROOT / "reference/PING_PONG_RULES.md", LOCAL / "rules/PING_PONG_RULES.md"),
    (ROOT / "docs/SPEC.md", LOCAL / "rules/SPEC_rules.md"),
    (ROOT / "reference/findings/time_patterns.md", LOCAL / "backtests/time_patterns.md"),
]:
    if src.exists():
        shutil.copy(src, dst)
        print("staged", dst.relative_to(ROOT))
# Placeholder: transcripts are ingested separately via scripts/ingest_transcripts.py (yt-dlp, optional).
(LOCAL / "transcripts/README.md").write_text(
    "# ICT transcripts\n\nRun `python scripts/ingest_transcripts.py --playlist <url>` to download "
    "and chunk YouTube transcripts. Do NOT commit downloaded content.\n")

bucket = os.environ.get("KB_BUCKET")
if not bucket:
    try:
        bucket = config.resource("KbBucket", "KB_BUCKET")
    except Exception as e:
        print(f"Local staging only (no KB_BUCKET / stack): {e}")
        sys.exit(0)
s3 = boto3.client("s3", region_name=config.AWS_REGION)
for path in LOCAL.rglob("*"):
    if path.is_file():
        key = str(path.relative_to(LOCAL))
        s3.upload_file(str(path), bucket, key)
        print(f"s3://{bucket}/{key}")
