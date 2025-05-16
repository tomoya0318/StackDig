from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class InlineComment(DataClassJsonMixin):
    """インラインコメント情報を表すデータクラス"""

    id: str
    revision_id: str
    author_id: int
    file_id: int
    line_number: int
    message: str
    created_at: datetime = field(
        metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat),
    )


class InlineCommentRepository:
    """インラインコメント用データベースを操作するためのリポジトリクラス"""

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
        self.queries_file = query_dir / "inline_comment_queries.sql"

    def create(self, inline_comment: InlineComment) -> str:
        """新しいインラインコメントを作成する

        Args:
            inline_comment (InlineComment): インラインコメント情報

        Returns:
            str: 作成されたインラインコメントのID

        """
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # SQLファイルからクエリを読み込み
        query = load_query_from_file(self.queries_file, "create_inline_comment")
        cursor.execute(
            query,
            (
                inline_comment.id,
                inline_comment.revision_id,
                inline_comment.author_id,
                inline_comment.file_id,
                inline_comment.line_number,
                inline_comment.message,
                inline_comment.created_at,
            ),
        )

        conn.commit()
        conn.close()

        return inline_comment.id
