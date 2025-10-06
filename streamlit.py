from dotenv import load_dotenv
import os
from langchain.globals import set_debug
from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import streamlit as st

load_dotenv()
#set_debug(True)

st.title("Bedrock Chat with Claude 4.5 Inference Profile")

chat = ChatBedrock(
  model_id=os.getenv("CLAUDE4.5_INFERENCE_PROFILE_ARN"),
  provider="anthropic",
  region_name=os.getenv("AWS_DEFAULT_REGION"),
  model_kwargs={
    "max_tokens": 1000,
  },
  streaming=True,
)

if "messages" not in st.session_state:
  st.session_state.messages = [
    SystemMessage(content="あなたのタスクはユーザーの質問に答えることです。"),
  ]

for message in st.session_state.messages:
  if message.type != "system":
    with st.chat_message(message.type):
      st.markdown(message.content)

if prompt := st.chat_input("質問を入力してください。"):
  st.session_state.messages.append(HumanMessage(content=prompt))

  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    response = st.write_stream(chat.stream(st.session_state.messages))
  st.session_state.messages.append(AIMessage(content=response))