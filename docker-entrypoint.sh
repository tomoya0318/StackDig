#!/bin/bash
set -e

# 必須環境変数のチェック
if [ -z "$CONTAINER_USER" ]; then
  echo "エラー: CONTAINER_USER 環境変数が設定されていません。.envファイルを確認してください。"
  exit 1
fi

if [ -z "$CONTAINER_PASSWORD" ]; then
  echo "エラー: CONTAINER_PASSWORD 環境変数が設定されていません。.envファイルを確認してください。"
  exit 1
fi

# 環境変数からユーザー名とパスワードを取得
USER_NAME=${CONTAINER_USER}
USER_PASSWORD=${CONTAINER_PASSWORD}

# ユーザーが存在するか確認し、存在しない場合は作成
if ! id -u "${USER_NAME}" >/dev/null 2>&1; then
  echo "User ${USER_NAME} does not exist. Creating..."
  groupadd -r ${USER_NAME}
  useradd -r -g ${USER_NAME} -m ${USER_NAME} -s /bin/bash
  echo "${USER_NAME}:${USER_PASSWORD}" | chpasswd
  mkdir -p /home/${USER_NAME}/.ssh
  chmod 700 /home/${USER_NAME}/.ssh
  chown -R ${USER_NAME}:${USER_NAME} /home/${USER_NAME}/.ssh
fi

# workディレクトリへのシンボリックリンクを作成（存在しない場合のみ）
if [ ! -e "/home/${USER_NAME}/work" ]; then
  ln -s /work /home/${USER_NAME}/work
  chown -h ${USER_NAME}:${USER_NAME} /home/${USER_NAME}/work
fi

# ログイン時に自動的に/workディレクトリに移動する設定
if ! grep -q "cd /work" "/home/${USER_NAME}/.bashrc"; then
  echo "# 自動的にプロジェクトディレクトリに移動" >> /home/${USER_NAME}/.bashrc
  echo "cd /work" >> /home/${USER_NAME}/.bashrc
fi

# SSHホスト鍵の永続化（Ed25519のみ）
mkdir -p /etc/ssh/host_keys

# 永続化された鍵があるか確認し、なければ生成して保存
if [ ! -f "/etc/ssh/host_keys/ssh_host_ed25519_key" ]; then
  echo "SSHホスト鍵(Ed25519)を生成しています..."
  ssh-keygen -t ed25519 -f /etc/ssh/host_keys/ssh_host_ed25519_key -N ""
fi

# 既存のキーを削除（もし存在すれば）して、新しい永続的な鍵にリンク
rm -f /etc/ssh/ssh_host_ed25519_key /etc/ssh/ssh_host_ed25519_key.pub
ln -sf /etc/ssh/host_keys/ssh_host_ed25519_key /etc/ssh/ssh_host_ed25519_key
ln -sf /etc/ssh/host_keys/ssh_host_ed25519_key.pub /etc/ssh/ssh_host_ed25519_key.pub

# SSH鍵の設定（オプション - あなたの公開鍵があれば）
if [ -f "/tmp/id_ed25519.pub" ]; then
  mkdir -p /home/${USER_NAME}/.ssh
  cat /tmp/id_ed25519.pub > /home/${USER_NAME}/.ssh/authorized_keys
  chmod 600 /home/${USER_NAME}/.ssh/authorized_keys
  chown -R ${USER_NAME}:${USER_NAME} /home/${USER_NAME}/.ssh

  # SSH設定を変更して公開鍵認証を有効にする
  sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
  # 必要に応じて他のSSH設定も変更
  # SSHサービスを再起動
  service ssh restart || /etc/init.d/ssh restart
fi

# SSHサーバーの起動
/usr/sbin/sshd

# UID/GIDの設定があれば実行
if [ ! -z "$HOST_UID" ] && [ ! -z "$HOST_GID" ]; then
  echo "Setting UID:GID for ${USER_NAME} to ${HOST_UID}:${HOST_GID}"
  groupmod -g $HOST_GID ${USER_NAME}
  usermod -u $HOST_UID ${USER_NAME}
fi

# 引数としてコマンドが渡された場合は実行
if [ "$1" = 'bash' ] || [ "$1" = 'python' ]; then
  exec gosu ${USER_NAME} "$@"
else
  exec "$@"
fi
