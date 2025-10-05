import os
from dotenv import load_dotenv
import boto3
from langchain_aws import ChatBedrock

load_dotenv()

REGION = os.getenv("AWS_DEFAULT_REGION")

client = boto3.client("bedrock", region_name=REGION)
models = client.list_foundation_models()["modelSummaries"]

claude_models = [m["modelId"] for m in models if "claude-3" in m["modelId"]]

if not claude_models:
    raise RuntimeError("Claude 3 系モデルが見つかりません。AWS Bedrockのリージョンとアクセス権を確認してください。")

print(f"Using models: {claude_models}")