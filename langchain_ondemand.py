from dotenv import load_dotenv
import os
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

chat = ChatBedrock(
  model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
  region_name="ap-northeast-1",
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