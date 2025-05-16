-- name: create_label_vote
INSERT INTO label_votes(revision_id, label_type_id, author_id, value, created_at)
VALUES(?, ?, ?, ?, ?);
-- end
