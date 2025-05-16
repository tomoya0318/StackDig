-- name: create_user
INSERT INTO users(name, display_name, email, created_at, updated_at)
VALUES(?, ?, ?, ?);
-- end
