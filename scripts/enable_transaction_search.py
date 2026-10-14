"""Enable CloudWatch Transaction Search (X-Ray spans -> CloudWatch Logs aws/spans), NovaMart pattern.
Idempotent. Never uses --disable-transaction-search."""
import json, sys, time
import boto3

REGION = "us-east-1"
SPANS, APP = "aws/spans", "/aws/application-signals/data"


def main(pct: int = 100):
    logs, xray = boto3.client("logs", region_name=REGION), boto3.client("xray", region_name=REGION)
    acct = boto3.client("sts").get_caller_identity()["Account"]
    try:
        logs.create_log_group(logGroupName=APP)
    except logs.exceptions.ResourceAlreadyExistsException:
        pass
    logs.put_resource_policy(policyName="TransactionSearchXRayAccess", policyDocument=json.dumps({
        "Version": "2012-10-17", "Statement": [{
            "Sid": "TransactionSearchXRayAccess", "Effect": "Allow", "Principal": {"Service": "xray.amazonaws.com"},
            "Action": "logs:PutLogEvents",
            "Resource": [f"arn:aws:logs:{REGION}:{acct}:log-group:{SPANS}:*", f"arn:aws:logs:{REGION}:{acct}:log-group:{APP}:*"],
            "Condition": {"ArnLike": {"aws:SourceArn": f"arn:aws:xray:{REGION}:{acct}:*"},
                          "StringEquals": {"aws:SourceAccount": acct}}}]}))

    def exists():
        return any(g["logGroupName"] == SPANS for g in logs.describe_log_groups(logGroupNamePrefix=SPANS)["logGroups"])

    def set_dest(d, timeout=180):
        end = time.time() + timeout
        while True:
            try:
                return xray.update_trace_segment_destination(Destination=d)
            except xray.exceptions.InvalidRequestException:
                if xray.get_trace_segment_destination().get("Destination") == d:
                    return
                if time.time() > end:
                    raise
                time.sleep(5)

    def wait(timeout=240):
        end = time.time() + timeout
        while time.time() < end:
            if exists():
                return
            time.sleep(5)
        raise TimeoutError("aws/spans not provisioned")

    dest = xray.get_trace_segment_destination()
    if dest.get("Destination") == "CloudWatchLogs" and not exists():
        set_dest("XRay"); set_dest("CloudWatchLogs"); wait()
    elif dest.get("Destination") != "CloudWatchLogs":
        set_dest("CloudWatchLogs"); wait()
    xray.update_indexing_rule(Name="Default", Rule={"Probabilistic": {"DesiredSamplingPercentage": pct}})
    d = xray.get_trace_segment_destination()
    print({"destination": d["Destination"], "status": d["Status"], "aws_spans": exists(), "indexing_percent": pct})


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 100)
