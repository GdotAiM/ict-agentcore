"""Infra/CI/repo hygiene checks (NovaMart parity)."""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_aws_targets_empty():
    assert json.loads((ROOT / "agentcore/aws-targets.json").read_text()) == []


def test_gitignore_never_unignores_env():
    gi = (ROOT / ".gitignore").read_text().splitlines()
    assert ".env" in gi
    assert not any(l.strip().startswith("!.env") and l.strip() != "!.env.example" for l in gi)


def test_ci_workflow():
    wf = (ROOT / ".github/workflows/offline-tests.yml").read_text()
    for s in ("actions/checkout@v7", "actions/setup-python@v7", "ubuntu-24.04", "gitleaks", "pytest"):
        assert s in wf


def test_stack_resources():
    y = (ROOT / "infrastructure/stack.yaml").read_text() + (ROOT / "infrastructure/schedules.yaml").read_text()
    for s in ("AWS::S3Vectors::VectorBucket", "AWS::S3Vectors::Index", "Dimension: 1024", "trade-state",
              "agent-sessions", "AWS::Scheduler::Schedule", "ScheduleExpressionTimezone: America/New_York",
              "xray:PutTraceSegments", "bedrock:ApplyGuardrail"):
        assert s in y


def test_no_owner_equity_or_client_name_hardcoded():
    """Keep equity and the former client name out of the published tree."""
    import subprocess
    forbidden = "hilda"
    for p in (ROOT / "ict_pipeline").rglob("*.py"):
        t = p.read_text()
        assert forbidden not in t.lower(), p
        assert not re.search(r"EQUITY\s*=\s*\d", t), p
    skip = {"tests/test_repo_hygiene.py"}
    for rel in subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines():
        if rel in skip:
            continue
        path = ROOT / rel
        try:
            t = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        assert forbidden not in t.lower(), rel


def test_kill_zone_crons_cover_zones():
    from ict_pipeline.killzones import schedule_crons
    assert len(schedule_crons()) >= 5
