import os
import boto3
from dotenv import load_dotenv
from langchain.globals import set_debug
from langchain_aws import ChatBedrock
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import streamlit as st

load_dotenv()
set_debug(True)

boto3.setup_default_session(region_name="us-east-1")

retriever = AmazonKnowledgeBasesRetriever(
  knowledge_base_id=os.getenv("KNOWLEDGE_BASE_ID"),
  retrieval_config={
    "vectorSearchConfiguration": {"numberOfResults": 10}
  }
)

prompt = ChatPromptTemplate.from_template(
  "以下のcontextに基づいて回答してください： {context} / 質問： {question}"
)

model = ChatBedrock(
  model_id=os.getenv("CLAUDE4.5_INFERENCE_PROFILE_USEAST1_ARN"),
  provider="anthropic",
  region_name="us-east-1",
  model_kwargs={
    "max_tokens": 1000,
  },
)

chain = (
  {"context": retriever, "question": RunnablePassthrough()}
  | prompt
  | model
  | StrOutputParser()
)

st.title("両国のカフェにちょっと詳しいClaude君")
question = st.text_input("質問を入力してください")
button = st.button("質問する")

if button:
  st.write(chain.invoke(question))