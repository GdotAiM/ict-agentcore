"""End-to-end deploy (mirrors NovaMart's flow). Requires AWS credentials + AgentCore CLI (npm).
NOTHING here places trades or talks to a broker.

    python scripts/deploy.py --all            # every step below
    python scripts/deploy.py --step stack     # one step

Steps: stack -> seed -> kb -> guardrail -> memory -> stage -> agentcore -> invoker -> schedules -> dashboard
"""
import argparse, json, os, shutil, string, subprocess, sys, zipfile, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from dotenv import load_dotenv; load_dotenv(os.path.join(ROOT, ".env"))

PROJECT = os.environ.get("PROJECT_NAME", "ict-agentcore")
REGION = os.environ.get("AWS_REGION", "us-east-1")
STEPS = ["stack", "seed", "kb", "guardrail", "memory", "stage", "agentcore", "invoker", "schedules", "dashboard"]


def sh(cmd, **kw):
    print("+", " ".join(cmd)); subprocess.run(cmd, check=True, cwd=kw.get("cwd", ROOT))


def step_stack():
    sh(["aws", "cloudformation", "deploy", "--stack-name", PROJECT, "--template-file", "infrastructure/stack.yaml",
        "--capabilities", "CAPABILITY_NAMED_IAM", "--parameter-overrides", f"ProjectName={PROJECT}", "--region", REGION])


def step_seed():
    sh([sys.executable, "scripts/seed_kb_docs.py"])


def step_kb():
    sh([sys.executable, "scripts/create_knowledge_bases.py"])


def step_guardrail():
    sh([sys.executable, "scripts/create_guardrail.py"])


def step_memory():
    sh([sys.executable, "scripts/create_memory.py"])


RUNTIME_DEPS = [
    "strands-agents>=1.0", "bedrock-agentcore>=0.1", "boto3>=1.42", "python-dotenv>=1.0",
    "pydantic>=2.6", "yfinance>=0.2.50", "pandas>=2.0",
    # tvdatafeed (git-only, no PyPI release) is vendored into build/runtime/ by step_stage; these are its deps.
    "requests>=2.31", "websocket-client>=1.6", "setuptools",
]
TVDATAFEED_GIT = "git+https://github.com/rongardF/tvdatafeed.git"


def step_stage():
    out = os.path.join(ROOT, "build", "runtime")
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "ict_pipeline"), os.path.join(out, "ict_pipeline"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(os.path.join(ROOT, "agentcore", "main.py"), out)
    try:  # vendor tvDatafeed (pure python) so TV:OANDA is the primary source in the runtime
        sh([sys.executable, "-m", "pip", "install", "-q", "--no-deps", "--target", os.path.join(out, "_vendor"), TVDATAFEED_GIT])
        shutil.move(os.path.join(out, "_vendor", "tvDatafeed"), os.path.join(out, "tvDatafeed"))
        shutil.rmtree(os.path.join(out, "_vendor"), ignore_errors=True)
    except Exception as e:
        print("WARN: tvdatafeed not vendored, runtime will use yfinance fallback:", e)
    deps = ",\n".join(f'  "{d}"' for d in RUNTIME_DEPS)
    open(os.path.join(out, "pyproject.toml"), "w").write(
        '[project]\nname = "ict-agentcore-runtime"\nversion = "0.1.0"\n'
        'description = "ICT analysis-only pipeline (AgentCore Runtime package)"\n'
        f'requires-python = ">=3.12"\ndependencies = [\n{deps},\n]\n')
    load_dotenv(os.path.join(ROOT, ".env"), override=True)
    from ict_pipeline import config
    keys = ["OWNER_NAME", "EQUITY", "ALERT_CHANNEL", "RULES_KB_ID", "TRANSCRIPTS_KB_ID", "BACKTESTS_KB_ID",
            "GUARDRAIL_ID", "GUARDRAIL_VERSION", "AGENTCORE_MEMORY_ID", "DAILY_TOKEN_BUDGET"]
    env = {k: os.environ.get(k, "").split("#")[0].strip() for k in keys}
    env["ALERT_CHANNEL"] = env["ALERT_CHANNEL"] or "file"
    env["DAILY_TOKEN_BUDGET"] = env["DAILY_TOKEN_BUDGET"] or "2000000"
    env.update(AWS_REGION=REGION, PROJECT_NAME=PROJECT,
               AGENTCORE_ROLE_ARN=config.resource("AgentCoreRoleArn", "AGENTCORE_ROLE_ARN"))
    spec = json.loads(string.Template(open(os.path.join(ROOT, "agentcore", "agentcore.template.json")).read())
                      .safe_substitute(env))
    rt = spec["runtimes"][0]
    rt["envVars"] = [e for e in rt["envVars"] if e["value"] != ""]   # EQUITY stays unset when blank
    rt["envVars"] += [{"name": "ALERT_DIR", "value": "/tmp/alerts"}, {"name": "LOG_DIR", "value": "/tmp/logs"},
                      {"name": "TRADE_STATE_TABLE", "value": config.trade_state_table()},
                      {"name": "OPS_TABLE", "value": config.ops_table()},
                      {"name": "SNAPSHOT_BUCKET", "value": config.snapshot_bucket()},
                      {"name": "ALERT_BUCKET", "value": config.snapshot_bucket()},
                      {"name": "NEWS_CALENDAR_PATH", "value": "ict_pipeline/data/news_calendar.json"}]
    json.dump(spec, open(os.path.join(ROOT, "agentcore", "agentcore.json"), "w"), indent=2)
    account = __import__("boto3").client("sts").get_caller_identity()["Account"]
    json.dump([{"name": "default", "account": account, "region": REGION}],
              open(os.path.join(ROOT, "agentcore", "aws-targets.json"), "w"), indent=2)
    print("staged build/runtime and agentcore/agentcore.json (aws-targets.json filled locally; do NOT commit it)")


def step_agentcore():
    sh(["agentcore", "deploy", "-y"], cwd=os.path.join(ROOT))
    state = os.path.join(ROOT, "agentcore", ".cli", "deployed-state.json")
    arn = ""
    try:
        for t in json.load(open(state)).get("targets", {}).values():
            for rt in ((t.get("resources") or {}).get("runtimes") or {}).values():
                arn = rt.get("runtimeArn") or arn
    except Exception:
        pass
    if arn:
        envp = os.path.join(ROOT, ".env")
        lines = [l for l in open(envp).read().splitlines() if not l.startswith("AGENTCORE_RUNTIME_ARN=")]
        open(envp, "w").write("\n".join(lines + [f"AGENTCORE_RUNTIME_ARN={arn}"]) + "\n")
        os.environ["AGENTCORE_RUNTIME_ARN"] = arn
    print("AGENTCORE_RUNTIME_ARN =", arn or "(not found; run agentcore status)")


def step_invoker():
    import boto3
    from ict_pipeline import config
    lam = boto3.client("lambda", region_name=REGION)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.write(os.path.join(ROOT, "scripts", "cycle_invoker_lambda.py"), "handler.py")
    name = f"{PROJECT}-cycle-invoker"
    env = {"Variables": {"AGENTCORE_RUNTIME_ARN": os.environ["AGENTCORE_RUNTIME_ARN"]}}
    try:
        lam.update_function_code(FunctionName=name, ZipFile=buf.getvalue())
        lam.update_function_configuration(FunctionName=name, Environment=env)
    except lam.exceptions.ResourceNotFoundException:
        lam.create_function(FunctionName=name, Runtime="python3.12", Handler="handler.handler", Timeout=300,
                            Role=config.resource("AgentCoreRoleArn", "AGENTCORE_ROLE_ARN"),
                            Code={"ZipFile": buf.getvalue()}, Environment=env)
    print("invoker lambda ready:", name)


def _ny_to_utc_cron(minutes: str, hours_ny: range, days: str) -> str:
    """EventBridge *Rules* are UTC-only; convert NY hours using today's NY UTC offset (re-run after DST)."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    off = int(-datetime.now(ZoneInfo("America/New_York")).utcoffset().total_seconds() // 3600)
    hrs = sorted({(h + off) % 24 for h in hours_ny})
    return f"cron({minutes} {','.join(map(str, hrs))} ? * {days} *)"


def step_schedules():
    """Preferred: EventBridge Scheduler stack (America/New_York tz, DST-safe).
    Fallback (sandbox denies scheduler:*): classic EventBridge Rules in UTC, created DISABLED."""
    import boto3
    try:
        sh(["aws", "cloudformation", "deploy", "--stack-name", f"{PROJECT}-schedules", "--template-file",
            "infrastructure/schedules.yaml", "--capabilities", "CAPABILITY_NAMED_IAM",
            "--parameter-overrides", f"ProjectName={PROJECT}", "--region", REGION])
        print("EventBridge Scheduler stack deployed (schedules DISABLED by design)")
        return
    except subprocess.CalledProcessError:
        print("Scheduler stack failed (likely scheduler:* denied). Falling back to EventBridge Rules.")
        subprocess.run(["aws", "cloudformation", "delete-stack", "--stack-name", f"{PROJECT}-schedules",
                        "--region", REGION])
    ev = boto3.client("events", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    fn = lam.get_function(FunctionName=f"{PROJECT}-cycle-invoker")["Configuration"]["FunctionArn"]
    rules = {  # name: (minutes, NY hours, days, kill zone)
        "asian": ("0/5", range(20, 24), "MON-FRI", "ASIAN"),  # UTC day after the NY Sun-Thu evening
        "london-open": ("0/5", range(2, 5), "MON-FRI", "LONDON_OPEN"),
        "ny-am": ("0/5", range(7, 10), "MON-FRI", "NY_AM"),
        "sb-lc": ("0/5", range(10, 12), "MON-FRI", "SILVER_BULLET"),
        "ny-pm": ("0/5", range(13, 16), "MON-FRI", "NY_PM"),
    }
    for n, (m, hrs, days, kz) in rules.items():
        name = f"{PROJECT}-kz-{n}"
        arn = ev.put_rule(Name=name, ScheduleExpression=_ny_to_utc_cron(m, hrs, days), State="DISABLED",
                          Description=f"{kz} kill zone (UTC; NY offset at deploy time)")["RuleArn"]
        ev.put_targets(Rule=name, Targets=[{"Id": "invoker", "Arn": fn, "Input": json.dumps({"kill_zone": kz})}])
        try:
            lam.add_permission(FunctionName=fn, StatementId=f"events-{n}", Action="lambda:InvokeFunction",
                               Principal="events.amazonaws.com", SourceArn=arn)
        except lam.exceptions.ResourceConflictException:
            pass
        print("rule", name, "DISABLED", _ny_to_utc_cron(m, hrs, days))
    print("Enable with: aws events enable-rule --name <rule>  (re-run --step schedules after 1 Nov DST change)")


def step_dashboard():
    sh([sys.executable, "scripts/cloudwatch_dashboard.py"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--step", choices=STEPS)
    a = ap.parse_args()
    steps = STEPS if a.all else [a.step] if a.step else []
    if not steps:
        ap.print_help(); return
    for s in steps:
        print(f"\n=== {s} ==="); globals()[f"step_{s}"]()


if __name__ == "__main__":
    main()
