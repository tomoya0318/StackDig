-- name: create_label_type
INSERT INTO label_types(name, min_value, max_value, description)
VALUES(?, ?, ?, ?);
-- end
