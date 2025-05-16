from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class LabelVote(DataClassJsonMixin):
    """ラベル情報を表すデータクラス"""

    id: int
    revision_id: str
    label_type_id: int
    author_id: int
    value: int
    created_at: datetime = field(
        metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat),
    )


class LabelVoteRepository:
    """ラベル用データベースを操作するためのリポジトリクラス"""

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
        self.queries_file = query_dir / "label_vote_queries.sql"

    def create(self, label_vote: LabelVote) -> int | None:
        """新しいラベル投票を作成する

        Args:
            label_vote (LabelVote): ラベル投票情報

        Returns:
            int: 作成されたラベル投票のID

        """
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # SQLファイルからクエリを読み込み
        query = load_query_from_file(self.queries_file, "create_label_vote")
        cursor.execute(
            query,
            (
                label_vote.revision_id,
                label_vote.label_type_id,
                label_vote.author_id,
                label_vote.value,
                label_vote.created_at,
            ),
        )

        # 作成されたラベル投票のIDを取得
        label_vote_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return label_vote_id
