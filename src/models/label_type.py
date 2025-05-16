from dataclasses import dataclass
from pathlib import Path

from dataclasses_json import DataClassJsonMixin, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class LabelType(DataClassJsonMixin):
    """ラベル種類を表すデータクラス"""

    id: int
    name: str
    min_value: int
    max_value: int
    description: str


class LabelTypeRepository:
    """ラベル種類用データベースを操作するためのリポジトリクラス"""

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
                label_type.description,
            ),
        )

        # 作成されたラベルタイプのIDを取得
        label_type_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return label_type_id
