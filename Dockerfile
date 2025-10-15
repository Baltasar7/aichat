# ベースイメージ
FROM --platform=linux/amd64 python:3.12-slim

# 作業ディレクトリ
WORKDIR /app

# デバッガ
RUN apt-get update && apt-get install -y \
    iproute2 \
    procps \
    curl \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# 依存パッケージ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体
COPY langchain_streamlit_knowledge_base.py .
COPY .env .

# Streamlit のポート設定
EXPOSE 8501

# 起動コマンド
CMD ["streamlit", "run", "langchain_streamlit_knowledge_base.py", "--server.port=8501", "--server.address=0.0.0.0"]
