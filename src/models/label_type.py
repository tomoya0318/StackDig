from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class LabelType(DataClassJsonMixin):
    id: int
    name: str
    min_value: int
    max_value: int
    description: str


class LabelTypeRepository:
    def __init__(self, db_path=DB_PATH, query_dir=QUERY_DIR):
        self.db_path = db_path
        self.queries_file = query_dir / "label_type_queries.sql"

    def create(self, label_type: LabelType) -> int | None:
        """新しいラベルタイプを作成する

        Args:
            label_type (LabelType): ラベルタイプ情報

        Returns:
            int: 作成されたラベルタイプのID
        """
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # SQLファイルからクエリを読み込み
        query = load_query_from_file(self.queries_file, "create_label_type")
        cursor.execute(
            query,
            (
                label_type.name,
                label_type.min_value,
                label_type.max_value,
                label_type.description
            )
        )

        # 作成されたラベルタイプのIDを取得
        label_type_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return label_type_id
