"""CloudWatch dashboard + GetMetricWidgetImage PNG (NovaMart pattern).

    python scripts/cloudwatch_dashboard.py [--hours 3] [--png docs/screenshots/dashboard.png]
"""
import io, json, os, sys, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from dotenv import load_dotenv; load_dotenv(os.path.join(ROOT, ".env"))
import boto3

REGION = os.environ.get("AWS_REGION", "us-east-1")
PROJECT = os.environ.get("PROJECT_NAME", "ict-agentcore")
NAME = "ICT-Pipeline"
NS = os.environ.get("METRIC_NAMESPACE", "ICT/Pipeline")
AGENTS = ["bias", "timeframe", "intermarket", "liquidity", "orderflow",
          "entry_model", "scalp", "pingpong", "confluence", "probability", "mentor"]
MODELS = {"Orchestrator (Haiku 4.5)": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
          "Workers (Sonnet 4.5)": "us.anthropic.claude-sonnet-4-5-20250929-v1:0"}


def widgets(account, guardrail_id, guardrail_version, runtime_arn):
    g_arn = f"arn:aws:bedrock:{REGION}:{account}:guardrail/{guardrail_id}"
    rt_name = f"{PROJECT.replace('-', '_')}_runtime::DEFAULT"
    rt_dims = ["Resource", runtime_arn, "Operation", "InvokeAgentRuntime", "Name", rt_name]
    base = {"region": REGION, "view": "timeSeries", "stacked": False, "period": 300}
    inv = [[NS, "AgentInvocations", "Agent", a, {"stat": "Sum", "label": a}] for a in AGENTS]
    inv += [["AWS/Bedrock", "Invocations", "ModelId", m, {"stat": "Sum", "label": f"Bedrock {k}"}]
            for k, m in MODELS.items()]
    lat = [[NS, "AgentLatencyMs", "Agent", a, {"stat": "Average", "label": a}] for a in AGENTS]
    gr = [["AWS/Bedrock/Guardrails", "Invocations", "GuardrailArn", g_arn, "GuardrailVersion", guardrail_version,
           {"stat": "Sum", "label": "Guardrail evaluations"}],
          ["AWS/Bedrock/Guardrails", "InvocationsIntervened", "GuardrailArn", g_arn, "GuardrailVersion", guardrail_version,
           {"stat": "Sum", "label": "Guardrail interventions"}]]
    rules = [[NS, "RuleBlocked", "Reason", r, {"stat": "Sum", "label": r}]
             for r in ["RR_BELOW_2", "STOP_TOO_TIGHT", "RISK_UNIT_FULL", "OPPOSITE_OPEN",
                       "NEWS_BLACKOUT", "FORMING_CANDLE", "DUPLICATE"]]
    health = [["AWS/Bedrock-AgentCore", "Latency", *rt_dims, {"stat": "Average", "label": "Runtime latency (avg ms)"}],
              ["AWS/Bedrock-AgentCore", "SystemErrors", *rt_dims, {"stat": "Sum", "yAxis": "right"}],
              ["AWS/Bedrock-AgentCore", "UserErrors", *rt_dims, {"stat": "Sum", "yAxis": "right"}]]
    return [("Invocations over time", inv), ("Average latency per agent (ms)", lat),
            ("Guardrail trigger frequency", gr), ("Rule blocks by reason", rules),
            ("AgentCore runtime health", health)], base


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--hours", type=int, default=3)
    ap.add_argument("--png", default=os.path.join(ROOT, "docs", "screenshots", "dashboard", "cloudwatch-dashboard.png"))
    ap.add_argument("--no-iam", action="store_true"); a = ap.parse_args()
    account = boto3.client("sts").get_caller_identity()["Account"]
    gid, gver = os.environ["GUARDRAIL_ID"], os.environ["GUARDRAIL_VERSION"]
    runtime_arn = os.environ["AGENTCORE_RUNTIME_ARN"]
    if not a.no_iam:
        boto3.client("iam").put_role_policy(
            RoleName=f"{PROJECT}-agentcore-role", PolicyName="ICTCustomMetrics",
            PolicyDocument=json.dumps({"Version": "2012-10-17", "Statement": [{
                "Effect": "Allow", "Action": "cloudwatch:PutMetricData", "Resource": "*",
                "Condition": {"StringEquals": {"cloudwatch:namespace": NS}}}]}))
    ws, base = widgets(account, gid, gver, runtime_arn)
    body = {"widgets": [{"type": "metric", "width": 12, "height": 6, "x": 12 * (i % 2), "y": 6 * (i // 2),
                         "properties": {**base, "title": t, "metrics": m}} for i, (t, m) in enumerate(ws)]}
    cw = boto3.client("cloudwatch", region_name=REGION)
    cw.put_dashboard(DashboardName=NAME, DashboardBody=json.dumps(body))
    print(f"Dashboard: https://{REGION}.console.aws.amazon.com/cloudwatch/home?region={REGION}#dashboards/dashboard/{NAME}")
    try:
        from PIL import Image, ImageDraw, ImageFont
        imgs = []
        for t, m in ws:
            props = {**base, "title": t, "metrics": m, "width": 900, "height": 360,
                     "start": f"-PT{a.hours}H", "end": "P0D",
                     "timezone": os.environ.get("DASHBOARD_TZ", "+0200")}
            imgs.append(Image.open(io.BytesIO(
                cw.get_metric_widget_image(MetricWidget=json.dumps(props))["MetricWidgetImage"])).convert("RGB"))
        cols = 2; rows = (len(imgs) + 1) // 2
        w, h = imgs[0].size
        sheet = Image.new("RGB", (cols * w + 30, rows * h + 80), "white")
        ImageDraw.Draw(sheet).text((10, 15), f"CloudWatch {NAME} last {a.hours}h (GetMetricWidgetImage)", fill="black")
        for i, im in enumerate(imgs):
            sheet.paste(im, (10 + (i % cols) * (w + 10), 60 + (i // cols) * (h + 10)))
        os.makedirs(os.path.dirname(a.png), exist_ok=True); sheet.save(a.png); print("PNG:", a.png)
    except Exception as e:
        print("PNG export skipped:", e)


if __name__ == "__main__":
    main()
