import sqlite3
import warnings
from pathlib import Path

from src.config import DB_PATH


def get_db_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    # データベースに接続する
    conn = sqlite3.connect(db_path)

    # 取得結果を事象形式で受け取る
    conn.row_factory = sqlite3.Row

    # 外部キー制約を有効にする
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

def execute_sql_file(conn: sqlite3.Connection, sql_file_path: Path) -> sqlite3.Connection:
    # SQLファイルを読み込む
    with open(sql_file_path, "r") as file:
        sql_script = file.read()

    # SQLスクリプトを実行する
    conn.executescript(sql_script)

    return conn

def load_query_from_file(file_path: Path, query_name: str) -> str:
    # SQLファイルを読み込む
    with open(file_path, "r") as file:
        sql_script = file.read()

    # クエリを抽出する
    query_marker = f"-- name: {query_name}"
    end_marker = "-- end"
    if query_marker not in sql_script:
        raise ValueError(f"Query '{query_name}' not found in {file_path}")

    # クエリの開始位置を特定
    start_pos = sql_script.find(query_marker) + len(query_marker)

    # クエリの終了位置を特定
    end_pos = sql_script.find(end_marker, start_pos)

    if end_pos == -1:
        warnings.warn(f"End marker '{end_marker}' not found for query '{query_name}' in {file_path}")
        query = sql_script[start_pos:].strip()
    else:
        query = sql_script[start_pos:end_pos].strip()

    return query

