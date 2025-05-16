from dataclasses import dataclass
from pathlib import Path

from dataclasses_json import DataClassJsonMixin, dataclass_json

from config import DB_PATH, QUERY_DIR
from db.connection import get_db_connection, load_query_from_file


@dataclass_json
@dataclass
class File(DataClassJsonMixin):
    """ファイル情報を表すデータクラス"""

    id: int
    file_name: str
    file_path: str


class FileRepository:
    """ファイル用データベースを操作するためのリポジトリクラス"""

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
        self.queries_file = query_dir / "file_queries.sql"

    def create(self, file: File) -> int | None:
        """新しいファイルを作成する

        Args:
            file (File): ファイル情報

        Returns:
            int: 作成されたファイルのID

        """
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # SQLファイルからクエリを読み込み
        query = load_query_from_file(self.queries_file, "create_file")
        cursor.execute(query, (file.file_name, file.file_path))

        # 作成されたファイルのIDを取得
        file_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return file_id
