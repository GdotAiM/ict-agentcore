"""Ask the deployed pipeline one owner question through the Cognito-protected frontend Lambda URL.
Reads the test user from /workspace/.ict-cognito-test-user (never printed). Usage: python scripts/frontend_chat.py "question" """
import json, os, sys, urllib.request
import boto3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.loads(open(os.path.join(ROOT, "frontend", "config.js")).read().split("=", 1)[1].strip().rstrip(";"))
cred = json.load(open(os.environ.get("COGNITO_TEST_USER_FILE", os.path.join(os.path.dirname(ROOT), ".ict-cognito-test-user"))))
tok = boto3.client("cognito-idp", region_name=cfg["region"]).initiate_auth(
    ClientId=cfg["clientId"], AuthFlow="USER_PASSWORD_AUTH",
    AuthParameters={"USERNAME": cred["email"], "PASSWORD": cred["password"]})["AuthenticationResult"]["AccessToken"]
req = urllib.request.Request(cfg["proxyUrl"], data=json.dumps({"prompt": sys.argv[1]}).encode(), method="POST",
                             headers={"authorization": f"Bearer {tok}", "content-type": "application/json"})
print(urllib.request.urlopen(req, timeout=120).read().decode())
