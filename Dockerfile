# ベースイメージ
FROM --platform=linux/amd64 python:3.12-slim

# uv準備
RUN pip install uv
COPY pyproject.toml uv.lock /app/

# 作業ディレクトリ
WORKDIR /app

# デバッガ
RUN apt-get update && apt-get install -y \
    iproute2 \
    procps \
    curl \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# 依存パッケージ (uv)
RUN uv sync --frozen --no-cache

# アプリ本体
COPY --chmod=755 langchain_streamlit_knowledge_base.py .
COPY --chmod=644 .env .

# Streamlit のポート設定
EXPOSE 8501

# 起動コマンド (direct streamlit)
CMD ["uv", "run", "streamlit", "run", "langchain_streamlit_knowledge_base.py", "--server.port=8501", "--server.address=0.0.0.0"]