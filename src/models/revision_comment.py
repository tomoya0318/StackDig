from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class RevisionComment(DataClassJsonMixin):
    """リビジョンコメント情報を表すデータクラス"""

    id: str
    revision_id: str
    author_id: int
    message: str
    created_at: datetime = field(
        metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat),
    )


class RevisionCommentRepository:
    """リビジョンコメント用データベースを操作するためのリポジトリクラス"""

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
        self.queries_file = query_dir / "revision_comment_queries.sql"

    def create(self, revision_comment: RevisionComment) -> str:
        """新しいリビジョンコメントを作成する

        Args:
            revision_comment (RevisionComment): リビジョンコメント情報

        Returns:
            str: 作成されたリビジョンコメントのID

        """
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # SQLファイルからクエリを読み込み
        query = load_query_from_file(self.queries_file, "create_revision_comment")
        cursor.execute(
            query,
            (
                revision_comment.id,
                revision_comment.revision_id,
                revision_comment.author_id,
                revision_comment.message,
                revision_comment.created_at,
            ),
        )

        conn.commit()
        conn.close()

        return revision_comment.id
