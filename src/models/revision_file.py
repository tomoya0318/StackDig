from dataclasses import dataclass
from pathlib import Path

from dataclasses_json import DataClassJsonMixin, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class RevisionFile(DataClassJsonMixin):
    """リビジョンとファイルの中間テーブルを表すデータクラス"""

    revision_id: str
    file_id: int


class RevisionFileRepository:
    """リビジョンとファイルの中間テーブル用データベースを操作するためのリポジトリクラス"""

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
        self.queries_file = query_dir / "revision_files.sql"

    def create(self, revision_id: str, file_id: int) -> int | None:
        """リビジョンとファイルの関連を新規登録する

        Args:
            revision_id (str): リビジョンID
            file_id (int): ファイルID
            created_at (datetime): 作成日時

        Returns:
            int | None: 作成された関連のID

        """
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # SQLファイルからクエリを読み込み
        query = load_query_from_file(self.queries_file, "create_revision_file")
        cursor.execute(query, (revision_id, file_id))

        # 作成された関連のIDを取得
        revision_file_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return revision_file_id
