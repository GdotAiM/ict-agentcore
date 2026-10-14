"""Cognito user pool + Lambda function-URL proxy frontend (NovaMart extra #4).

Creates a Cognito pool, app client, an owner test user, a Lambda that proxies
authenticated requests to the AgentCore runtime, and writes frontend/config.js.
Analysis only: the proxy never talks to a broker.

    python scripts/create_cognito_frontend.py
    python scripts/create_cognito_frontend.py --delete
"""
import argparse, json, os, sys, time, secrets
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from dotenv import load_dotenv; load_dotenv()
import boto3
from ict_pipeline import config

PROJECT = config.PROJECT_NAME
REGION = config.AWS_REGION
POOL_NAME = f"{PROJECT}-owners"
LAMBDA_NAME = f"{PROJECT}-frontend-proxy"
ROLE_NAME = f"{PROJECT}-frontend-proxy-role"


PROXY_CODE = '''
import json, os, uuid, boto3
RUNTIME = os.environ["AGENTCORE_RUNTIME_ARN"]
cognito = boto3.client("cognito-idp")
agentcore = boto3.client("bedrock-agentcore")
DENY = ("api_key", "password", "place_order", "broker_login")

def handler(event, context):
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return _cors(200, "")
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    token = headers.get("authorization", "").removeprefix("Bearer ").strip()
    try:
        user = cognito.get_user(AccessToken=token)          # validates the Cognito access token
    except Exception:
        return _cors(401, json.dumps({"error": "unauthorized"}))
    try:
        payload = json.loads(event.get("body") or "{}")
    except Exception:
        return _cors(400, json.dumps({"error": "invalid json"}))
    if any(k in json.dumps(payload).lower() for k in DENY):
        return _cors(400, json.dumps({"error": "analysis only"}))
    sid = (payload.get("session_id") or str(uuid.uuid4())).ljust(33, "0")
    body = {"prompt": str(payload.get("prompt", ""))[:2000], "session_id": sid, "owner_sub": user["Username"]}
    r = agentcore.invoke_agent_runtime(agentRuntimeArn=RUNTIME, runtimeSessionId=sid,
                                       payload=json.dumps(body).encode())
    return _cors(200, r["response"].read().decode())

def _cors(code, body):
    return {"statusCode": code, "headers": {
        "content-type": "application/json",
        "access-control-allow-origin": "*",
        "access-control-allow-headers": "authorization,content-type",
        "access-control-allow-methods": "POST,OPTIONS"}, "body": body}
'''


def ensure_role(iam):
    try:
        arn = iam.get_role(RoleName=ROLE_NAME)["Role"]["Arn"]
    except iam.exceptions.NoSuchEntityException:
        arn = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps({"Version": "2012-10-17", "Statement": [{
                "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"}]})
        )["Role"]["Arn"]
        iam.attach_role_policy(RoleName=ROLE_NAME,
                               PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
        time.sleep(8)
    iam.put_role_policy(RoleName=ROLE_NAME, PolicyName="InvokeAgentRuntime", PolicyDocument=json.dumps({
        "Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "bedrock-agentcore:InvokeAgentRuntime",
                                                "Resource": os.environ.get("AGENTCORE_RUNTIME_ARN", "*") + "*"}]}))
    return arn


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--delete", action="store_true"); a = ap.parse_args()
    cognito = boto3.client("cognito-idp", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    iam = boto3.client("iam")
    if a.delete:
        for p in cognito.list_user_pools(MaxResults=20)["UserPools"]:
            if p["Name"] == POOL_NAME:
                cognito.delete_user_pool(UserPoolId=p["Id"]); print("deleted pool", p["Id"])
        try:
            lam.delete_function(FunctionName=LAMBDA_NAME); print("deleted lambda")
        except Exception:
            pass
        try:
            iam.delete_role_policy(RoleName=ROLE_NAME, PolicyName="InvokeAgentRuntime")
            iam.detach_role_policy(RoleName=ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
            iam.delete_role(RoleName=ROLE_NAME)
        except Exception:
            pass
        return
    # Pool
    pools = [p for p in cognito.list_user_pools(MaxResults=20)["UserPools"] if p["Name"] == POOL_NAME]
    if pools:
        pool_id = pools[0]["Id"]
    else:
        pool_id = cognito.create_user_pool(PoolName=POOL_NAME, AutoVerifiedAttributes=["email"],
                                           UsernameAttributes=["email"])["UserPool"]["Id"]
    clients = cognito.list_user_pool_clients(UserPoolId=pool_id)["UserPoolClients"]
    if clients:
        client_id = clients[0]["ClientId"]
    else:
        client_id = cognito.create_user_pool_client(
            UserPoolId=pool_id, ClientName=f"{PROJECT}-web",
            ExplicitAuthFlows=["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"],
            GenerateSecret=False)["UserPoolClient"]["ClientId"]
    owner = os.environ.get("OWNER_EMAIL", "ict-owner@example.com")
    pw = os.environ.get("COGNITO_TEST_PASSWORD") or ("Ict!" + secrets.token_urlsafe(12) + "9")
    # Sandbox roles may deny AdminSetUserPassword: create with a temporary password and answer
    # NEW_PASSWORD_REQUIRED through the public client flow (same approach as NovaMart).
    try:
        cognito.admin_delete_user(UserPoolId=pool_id, Username=owner)
    except Exception:
        pass
    tmp = "Tmp!" + secrets.token_urlsafe(10) + "7a"
    cognito.admin_create_user(UserPoolId=pool_id, Username=owner, TemporaryPassword=tmp, MessageAction="SUPPRESS",
                              UserAttributes=[{"Name": "email", "Value": owner},
                                              {"Name": "email_verified", "Value": "true"}])
    ch = cognito.initiate_auth(ClientId=client_id, AuthFlow="USER_PASSWORD_AUTH",
                               AuthParameters={"USERNAME": owner, "PASSWORD": tmp})
    if ch.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
        cognito.respond_to_auth_challenge(ClientId=client_id, ChallengeName="NEW_PASSWORD_REQUIRED",
                                          Session=ch["Session"],
                                          ChallengeResponses={"USERNAME": owner, "NEW_PASSWORD": pw})
    # Lambda
    role_arn = ensure_role(iam)
    import zipfile, io
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("handler.py", PROXY_CODE)
    code = buf.getvalue()
    env = {"Variables": {"AGENTCORE_RUNTIME_ARN": os.environ.get("AGENTCORE_RUNTIME_ARN", "pending")}}
    try:
        lam.update_function_code(FunctionName=LAMBDA_NAME, ZipFile=code)
        lam.get_waiter("function_updated_v2").wait(FunctionName=LAMBDA_NAME)
        lam.update_function_configuration(FunctionName=LAMBDA_NAME, Environment=env)
        fn = lam.get_function(FunctionName=LAMBDA_NAME)["Configuration"]["FunctionArn"]
    except lam.exceptions.ResourceNotFoundException:
        fn = lam.create_function(FunctionName=LAMBDA_NAME, Runtime="python3.12", Role=role_arn,
                                 Handler="handler.handler", Code={"ZipFile": code}, Timeout=30,
                                 Environment=env)["FunctionArn"]
    try:
        url = lam.get_function_url_config(FunctionName=LAMBDA_NAME)["FunctionUrl"]
    except Exception:
        url = lam.create_function_url_config(FunctionName=LAMBDA_NAME, AuthType="NONE",
                                             Cors={"AllowOrigins": ["*"], "AllowMethods": ["POST"],
                                                   "AllowHeaders": ["authorization", "content-type"]})["FunctionUrl"]
    try:
        lam.add_permission(FunctionName=LAMBDA_NAME, StatementId="FunctionURLAllowPublic",
                           Action="lambda:InvokeFunctionUrl", Principal="*",
                           FunctionUrlAuthType="NONE")
    except Exception:
        pass
    try:  # since Oct 2025 public function URLs also need lambda:InvokeFunction (via function URL only)
        lam.add_permission(FunctionName=LAMBDA_NAME, StatementId="FunctionURLInvokeAllowPublic",
                           Action="lambda:InvokeFunction", Principal="*", InvokedViaFunctionUrl=True)
    except Exception:
        pass
    os.makedirs(os.path.join(ROOT, "frontend"), exist_ok=True)
    cfg = {"region": REGION, "userPoolId": pool_id, "clientId": client_id, "proxyUrl": url, "ownerEmail": owner}
    open(os.path.join(ROOT, "frontend", "config.js"), "w").write("window.ICT_CONFIG = " + json.dumps(cfg, indent=2) + ";\n")
    cred_path = os.environ.get("COGNITO_TEST_USER_FILE", os.path.join(os.path.dirname(ROOT), ".ict-cognito-test-user"))
    fd = os.open(cred_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(json.dumps({"email": owner, "password": pw}))
    print(json.dumps(cfg, indent=2))
    print(f"Wrote frontend/config.js; test-user credentials at {cred_path} (outside web root, mode 600)")


if __name__ == "__main__":
    main()
