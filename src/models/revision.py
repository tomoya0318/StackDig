from dataclasses import dataclass
from pathlib import Path

from dataclasses_json import dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class Revision:
    """リビジョン情報を表すデータクラス"""

    revision_id: str
    change_id: str
    author_id: int
    commit_message: str
    revision_number: int
    created_at: str


class RevisionRepository:
    """リビジョン用データベースを操作するためのリポジトリクラス"""

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
        self.queries_file = query_dir / "revision_queries.sql"

    def create(self, revision: Revision) -> str | None:
        """新しいリビジョンを作成する

        Args:
            revision (Revision): リビジョン情報

        Returns:
            str | None: 作成されたリビジョンのID

        """
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # SQLファイルからクエリを読み込み
        query = load_query_from_file(self.queries_file, "create_revision")

        cursor.execute(
            query,
            (
                revision.revision_id,
                revision.change_id,
                revision.author_id,
                revision.commit_message,
                revision.revision_number,
                revision.created_at,
            ),
        )

        conn.commit()
        conn.close()

        return revision.revision_id
