-- name: create_inline_comment
INSERT INTO inline_comments(id, revision_id, author_id, file_id, line_number, message, created_at)
VALUES(?, ?, ?, ?, ?, ?, ?);
-- end
