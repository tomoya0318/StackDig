from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class LabelVote(DataClassJsonMixin):
    id: int
    revision_id: str
    label_type_id: int
    author_id: int
    value: int
    created_at: datetime = field(metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat))


class LabelVoteRepository:
    def __init__(self, db_path=DB_PATH, query_dir=QUERY_DIR):
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
                label_vote.created_at
            )
        )

        # 作成されたラベル投票のIDを取得
        label_vote_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return label_vote_id
