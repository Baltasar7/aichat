import os
import boto3
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.globals import set_debug
import streamlit as st

load_dotenv()
set_debug(True)

boto3.setup_default_session(region_name="ap-northeast-1")

st.title("Bedrock Chat with Claude 4.5 Inference Profile")

if "session_id" not in st.session_state:
  st.session_state.session_id = "session_id"

if "history" not in st.session_state:
  st.session_state.history = DynamoDBChatMessageHistory(
    table_name="BedrockChatSessionTable",
    session_id=st.session_state.session_id,
  )

print("debug: if chain block start")
if "chain" not in st.session_state:
  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", "あなたのタスクはユーザーの質問に対し明確に答えることです。"),
      MessagesPlaceholder(variable_name="messages"),
      MessagesPlaceholder(variable_name="human_message"),
    ]
  )

  chat = ChatBedrock(
    model_id=os.getenv("CLAUDE4.5_INFERENCE_PROFILE_APNE1_ARN"),
    provider="anthropic",
    region_name="ap-northeast-1",
    model_kwargs={
      "max_tokens": 1000,
    },
    streaming=True,
  )
  chain = prompt | chat
  st.session_state.chain = chain
print("debug: if chain block end")

if st.button("履歴クリア"):
  st.session_state.history.clear()

print("debug: for message block start")
for message in st.session_state.history.messages:
  with st.chat_message(message.type):
    st.markdown(message.content)
    print("debug: message.type chat st.markdown(message.content) done")
print("debug: for message block end")

print("debug: if prompt block start")
if prompt := st.chat_input("質問を入力してください。"):
  with st.chat_message("user"):
    st.markdown(prompt)
    print("debug: user chat st.markdown(prompt) done")

  with st.chat_message("assistant"):
    response = st.write_stream(
      st.session_state.chain.stream(
        {
          "messages": st.session_state.history.messages,
          "human_message": [HumanMessage(content=prompt)],
        },
        config={"configurable": {"session_id": st.session_state.session_id}},
      )
    )
    print("debug: assistant chat response set done")

  st.session_state.history.add_user_message(prompt)
  st.session_state.history.add_ai_message(response)
  print("debug: stored in DynamoDB")
print("debug: if prompt block end")