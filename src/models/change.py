from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class Change(DataClassJsonMixin):
    change_id: str
    title: str
    branch_name: str
    merged_at: datetime = field(metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat))


class ChangeRepository:
    def __init__(self, db_path=DB_PATH, query_dir=QUERY_DIR):
        self.db_path = db_path
        self.queries_file = query_dir / "change_queries.sql"

    def create(self, change: Change) -> str:
        """新しい変更を作成する

        Args:
            change (Change): 変更情報

        Returns:
            str: 作成された変更のID
        """
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # SQLファイルからクエリを読み込み
        query = load_query_from_file(self.queries_file, "create_change")
        cursor.execute(query, (change.change_id, change.title, change.branch_name, change.merged_at))

        conn.commit()
        conn.close()

        return change.change_id
