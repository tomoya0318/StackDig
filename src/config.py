from pathlib import Path

ROOT = Path(__file__).parents[2]

# データディレクトリ
DATA = ROOT / "data"
DB_DIR = ROOT / "db" # データベースのディレクトリ
DB_PATH = DATA / "database.db" # 保存するためのデータベースのパス
QUERY_DIR = DB_DIR / "queries" # SQLクエリのディレクトリ

# OSSのデータソース設定
OPENSTACK_API_URL = "https://review.opendev.org/a"
