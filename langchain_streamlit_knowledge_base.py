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

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
session = boto3.Session(
  aws_access_key_id=aws_access_key_id,
  aws_secret_access_key=aws_secret_access_key,
  region_name=aws_region
)

retriever = AmazonKnowledgeBasesRetriever(
  knowledge_base_id=os.getenv("KNOWLEDGE_BASE_ID"),
  client=session.client("bedrock-agent-runtime", region_name=aws_region),
  retrieval_config={
    "vectorSearchConfiguration": {"numberOfResults": 10}
  }
)

prompt = ChatPromptTemplate.from_template("""
あなたはAIアシスタントです。

次のcontextが質問に役立つかどうかをまず判断してください：
{context}

質問：
{question}

- contextが質問に関連する場合は、contextの情報を用いて回答してください。
- contextが質問に関連しない場合は、contextを無視して、通常の知識で回答してください。
- 必ず関連性に応じてcontextの使用有無を判断してください。
- 回答する際に、contextを利用したことや、無視したことを明示しないでください。
"""
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