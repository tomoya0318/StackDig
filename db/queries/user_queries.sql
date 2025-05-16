-- name: create_user
INSERT INTO users(name, email, created_at, updated_at)
VALUES(?, ?, ?, ?);
-- end
