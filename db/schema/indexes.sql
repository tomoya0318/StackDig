-- users テーブルのインデックス
CREATE INDEX IF NOT EXISTS idx_users_name ON users(name);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- changes テーブルのインデックス
CREATE INDEX IF NOT EXISTS idx_changes_project_name ON changes(project_name);
CREATE INDEX IF NOT EXISTS idx_changes_branch_name ON changes(branch_name);
CREATE INDEX IF NOT EXISTS idx_changes_status ON changes(status);

-- revisions テーブルのインデックス
CREATE INDEX IF NOT EXISTS idx_revisions_change_id ON revisions(change_id);
CREATE INDEX IF NOT EXISTS idx_revisions_author_id ON revisions(author_id);
CREATE INDEX IF NOT EXISTS idx_revisions_created_at ON revisions(created_at);

-- files テーブルのインデックス
CREATE INDEX IF NOT EXISTS idx_files_file_name ON files(file_name);
CREATE INDEX IF NOT EXISTS idx_files_file_path ON files(file_path);

-- revision_comments テーブルのインデックス
CREATE INDEX IF NOT EXISTS idx_revision_comments_revision_id ON revision_comments(revision_id);
CREATE INDEX IF NOT EXISTS idx_revision_comments_author_id ON revision_comments(author_id);

-- inline_comments テーブルのインデックス
CREATE INDEX IF NOT EXISTS idx_inline_comments_revision_id ON inline_comments(revision_id);
CREATE INDEX IF NOT EXISTS idx_inline_comments_file_id ON inline_comments(file_id);
CREATE INDEX IF NOT EXISTS idx_inline_comments_revision_file ON inline_comments(revision_id, file_id);
CREATE INDEX IF NOT EXISTS idx_files_path_name ON files(file_path, file_name);
