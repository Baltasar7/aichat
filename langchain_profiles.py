from dotenv import load_dotenv
import os
from langchain.globals import set_debug
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()
#set_debug(True)

chat = ChatBedrock(
  model_id=os.getenv("CLAUDE4.5_INFERENCE_PROFILE_APNE1_ARN"),
  provider="anthropic",
  region_name="ap-northeast-1",
  model_kwargs={
    "max_tokens": 1000,
  },
  streaming=True,
)

messages = [
  SystemMessage(content="あなたのタスクはユーザーの質問に答えることです。"),
  HumanMessage(content="東京の天気は？"),
]

for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)
print("")

#response = chat.invoke(messages)
#print(response.content)