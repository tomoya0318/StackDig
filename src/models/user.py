from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class User(DataClassJsonMixin):
    id: int
    name: str
    display_name: str
    email: str
    created_at: datetime = field(metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat))

# データベース操作用のクラス
class UserRepository:
    def __init__(self, db_path=DB_PATH, query_dir=QUERY_DIR):
        self.db_path = db_path
        self.queries_file = query_dir / "user_queries.sql"

    def create(self, name: str, display_name: str, email: str, created_at: datetime) -> int | None:
        """新しいユーザを作成する

        Args:
            name (str): ユーザ名
            email (str): メールアドレス
            created_at (datetime): 作成日時

        Returns:
            int | None: 作成されたユーザのID
        """
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # SQLファイルからクエリを読み込み
        query = load_query_from_file(self.queries_file, "create_user")

        cursor.execute(query, (name, display_name, email, created_at))

        # 作成されたユーザーのIDを取得
        user_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return user_id
