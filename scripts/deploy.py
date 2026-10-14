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


def step_stage():
    out = os.path.join(ROOT, "build", "runtime")
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "ict_pipeline"), os.path.join(out, "ict_pipeline"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(os.path.join(ROOT, "agentcore", "main.py"), out)
    shutil.copy(os.path.join(ROOT, "requirements-runtime.txt"), os.path.join(out, "requirements.txt"))
    load_dotenv(os.path.join(ROOT, ".env"), override=True)
    from ict_pipeline import config
    env = {k: os.environ.get(k, "") for k in ["OWNER_NAME", "EQUITY", "ALERT_CHANNEL", "RULES_KB_ID", "TRANSCRIPTS_KB_ID",
                                               "BACKTESTS_KB_ID", "GUARDRAIL_ID", "GUARDRAIL_VERSION",
                                               "AGENTCORE_MEMORY_ID", "DAILY_TOKEN_BUDGET"]}
    env.update(AWS_REGION=REGION, PROJECT_NAME=PROJECT,
               AGENTCORE_ROLE_ARN=config.resource("AgentCoreRoleArn", "AGENTCORE_ROLE_ARN"))
    tpl = string.Template(open(os.path.join(ROOT, "agentcore", "agentcore.template.json")).read())
    open(os.path.join(ROOT, "agentcore", "agentcore.json"), "w").write(tpl.safe_substitute(env))
    account = __import__("boto3").client("sts").get_caller_identity()["Account"]
    json.dump([{"name": "default", "account": account, "region": REGION}],
              open(os.path.join(ROOT, "agentcore", "aws-targets.json"), "w"), indent=2)
    print("staged build/runtime and agentcore/agentcore.json (aws-targets.json filled locally; keep it out of commits)")


def step_agentcore():
    sh(["agentcore", "deploy", "-y"], cwd=os.path.join(ROOT))
    print("Copy the runtime ARN into .env as AGENTCORE_RUNTIME_ARN (agentcore status).")


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


def step_schedules():
    import boto3
    sch = boto3.client("scheduler", region_name=REGION)
    for n in ["asian", "london-open", "ny-am", "sb-lc", "ny-pm"]:
        name = f"{PROJECT}-kz-{n}"
        s = sch.get_schedule(Name=name)
        keep = {k: s[k] for k in ["Name", "ScheduleExpression", "ScheduleExpressionTimezone", "FlexibleTimeWindow", "Target"]}
        sch.update_schedule(**keep, State="ENABLED")
        print("enabled", name)


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
