-- name: create_change
INSERT INTO changes(change_id, created_at, updated_at)
VALUES(?, ?, ?);
-- end
