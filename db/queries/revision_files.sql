-- name: create_revision_file
INSERT INTO revision_files(revision_id, file_id)
VALUES(?, ?);
-- end
