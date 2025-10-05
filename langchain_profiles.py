# このプログラムは実行失敗する。

from dotenv import load_dotenv
import os
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

chat = ChatBedrock(
  model_id=os.getenv("CLAUDE4.5_INFERENCE_PROFILE_ARN"),
  provider="anthropic",
  region_name=os.getenv("AWS_DEFAULT_REGION"),
  model_kwargs={
    "max_tokens": 1000,
  },
)

messages = [
  SystemMessage(content="あなたのタスクはユーザーの質問に答えることです。"),
  HumanMessage(content="東京の天気は？"),
]

response = chat.invoke(messages)

print(response.content)