-- name: create_revision_comment
INSERT INTO revision_comments(id, revision_id, author_id, message, created_at)
VALUES(?, ?, ?, ?, ?);
-- end
