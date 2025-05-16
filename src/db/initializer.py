from src.config import DB_PATH, DB_DIR
from src.db.connection import execute_sql_file, get_db_connection


class DatabaseInitializer:
    def __init__(self, db_path=DB_PATH, db_dir=DB_DIR):
        self.db_path = db_path
        self.db_dir = db_dir

    def initialize(self):
        # データベースとテーブルを初期化する
        conn = get_db_connection(self.db_path)

        try:
            # スキーマを適用
            schema_path = self.db_dir / "table.sql"
            execute_sql_file(conn, schema_path)

            # インデックスを適用
            index_path = self.db_dir / "indexes.sql"
            execute_sql_file(conn, index_path)

            conn.commit()
            print("データベースが初期化されました")
        except Exception as e:
            print(f"データベースの初期化中にエラーが発生しました: {e}")
            raise
        finally:
            conn.close()
            print("データベース接続を閉じました")
