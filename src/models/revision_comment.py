from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class RevisionComment(DataClassJsonMixin):
    id: str
    revision_id: str
    author_id: int
    message: str
    created_at: datetime = field(metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat))


class RevisionCommentRepository:
    def __init__(self, db_path=DB_PATH, query_dir=QUERY_DIR):
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
                revision_comment.created_at
            )
        )

        conn.commit()
        conn.close()

        return revision_comment.id
