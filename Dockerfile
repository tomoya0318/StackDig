# -------------------------------------------------------------
# 1. ベースイメージ: Python 3.12 Slim
# -------------------------------------------------------------
    FROM python:3.12-slim-bookworm AS base

# ビルド引数を定義
ARG CONTAINER_USER
ARG CONTAINER_PASSWORD


ENV CONTAINER_USER=${CONTAINER_USER}
ENV CONTAINER_PASSWORD=${CONTAINER_PASSWORD}

# タイムゾーン設定
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# SSHサーバのインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-server \
    git \
    && mkdir -p /var/run/sshd \
    && mkdir -p /root/.ssh \
    && chmod 700 /root/.ssh \
    && echo "PermitRootLogin no" >> /etc/ssh/sshd_config \
    && echo "PasswordAuthentication no" >> /etc/ssh/sshd_config \
    && echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------
# 2. ビルドステージ: 依存関係のインストール
# -------------------------------------------------------------
FROM base AS builder

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    procps \
    gosu \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# requirements.txtのみを先にコピーしてキャッシュ活用
WORKDIR /work
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------------------
# 3. 実行ステージ: 最終イメージの作成
# -------------------------------------------------------------
FROM base

# 実行に必要なパッケージのみインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    procps \
    gosu \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# セキュリティ: 非rootユーザーの作成とSSH設定
RUN groupadd -r ${CONTAINER_USER} && useradd -r -g ${CONTAINER_USER} -m ${CONTAINER_USER} -s /bin/bash \
    && echo "${CONTAINER_USER}:${CONTAINER_PASSWORD}" | chpasswd \
    && mkdir -p /home/${CONTAINER_USER}/.ssh \
    && chmod 700 /home/${CONTAINER_USER}/.ssh \
    && chown -R ${CONTAINER_USER}:${CONTAINER_USER} /home/${CONTAINER_USER}/.ssh

# ビルドステージから必要なファイルをコピー
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# エントリーポイントスクリプトのコピー
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 環境変数設定 - ビルド時に固定される設定
ENV PYTHONPATH=/work/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 作業ディレクトリ設定
WORKDIR /work

# アプリケーションコードをコピー
COPY . /work/

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["bash"]
