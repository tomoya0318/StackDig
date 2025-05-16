from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class Change(DataClassJsonMixin):
    """変更情報を表すデータクラス"""

    change_id: str
    title: str
    branch_name: str
    merged_at: datetime = field(
        metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat),
    )


class ChangeRepository:
    """変更情報用データベースを操作するためのリポジトリクラス"""

    def __init__(self, db_path: Path = DB_PATH, query_dir: Path = QUERY_DIR):
        """リポジトリの初期化

        Args:
            db_path (Path, optional):
                データベースのパス.
                指定されていない場合はデフォルトで用意したパスを使用する.
            query_dir (Path, optional):
                クエリ用ディレクトリへのパス.
                指定されていない場合はデフォルトで用意したパスを使用する.

        """
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
        cursor.execute(
            query,
            (change.change_id, change.title, change.branch_name, change.merged_at),
        )

        conn.commit()
        conn.close()

        return change.change_id
