-- テーブル定義

-- ユーザテーブル
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    email VARCHAR(255),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- チェンジテーブル
CREATE TABLE IF NOT EXISTS changes (
    change_id VARCHAR(255) PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    branch_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    merged_at DATETIME
);

-- リビジョンテーブル
CREATE TABLE IF NOT EXISTS revisions (
    revision_id VARCHAR(255) PRIMARY KEY,
    change_id VARCHAR(255) NOT NULL,
    author_id INTEGER,
    commit_message TEXT,
    revision_number INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    UNIQUE (change_id, revision_number),
    FOREIGN KEY (change_id) REFERENCES changes(change_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ファイルテーブル
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    UNIQUE (file_path, file_name)
);

-- リビジョン-ファイル関連テーブル
CREATE TABLE IF NOT EXISTS revision_files (
    revision_id VARCHAR(255) NOT NULL,
    file_id INTEGER NOT NULL,
    PRIMARY KEY (revision_id, file_id),
    FOREIGN KEY (revision_id) REFERENCES revisions(revision_id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);

-- レビューコメントテーブル(リビジョンごと)
CREATE TABLE IF NOT EXISTS revision_comments (
    id VARCHAR(255) PRIMARY KEY,
    revision_id VARCHAR(255) NOT NULL,
    author_id INTEGER,
    message TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (revision_id) REFERENCES revisions(revision_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);

-- インラインコメントテーブル
CREATE TABLE IF NOT EXISTS inline_comments (
    id VARCHAR(255) PRIMARY KEY,
    revision_id VARCHAR(255) NOT NULL,
    author_id INTEGER,
    file_id INTEGER NOT NULL,
    line_number INTEGER NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (revision_id) REFERENCES revisions(revision_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
)

-- ラベルの種類テーブル
CREATE TABLE IF NOT EXISTS label_types (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,        -- Code-Review, Verified など
    min_value INTEGER NOT NULL,
    max_value INTEGER NOT NULL,
    description TEXT,
    UNIQUE (name)
);

-- ラベル評価テーブル
CREATE TABLE IF NOT EXISTS label_votes (
    revision_id VARCHAR(255) NOT NULL,
    label_type_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    value INTEGER NOT NULL, -- 評価値
    created_at DATETIME NOT NULL,
    PRIMARY KEY (revision_id, label_type_id, author_id),
    FOREIGN KEY (revision_id) REFERENCES revisions(revision_id) ON DELETE CASCADE,
    FOREIGN KEY (label_type_id) REFERENCES label_types(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);
