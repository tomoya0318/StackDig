-- name: create_file
INSERT INTO files(file_name, file_path)
VALUES(?, ?);
-- end
