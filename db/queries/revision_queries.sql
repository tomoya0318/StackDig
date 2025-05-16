-- name: create_revision
INSERT INTO revisions(change_id, author_id, commit_message, revision_number, created_at)
VALUES(?, ?, ?, ?, ?);
-- end
