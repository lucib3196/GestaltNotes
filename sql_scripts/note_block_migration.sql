BEGIN;


-- Copy the rows. This does not copy foreign keys or indexes.
CREATE TEMP TABLE note_block_test ON COMMIT DROP AS
SELECT * FROM note_block;

ALTER TABLE note_block_test
ADD COLUMN course_note_id uuid;

-- Map the existing course/file pair to its course note.
UPDATE note_block_test AS nb
SET course_note_id = cn.id
FROM course_note AS cn
WHERE cn.course_id = nb.course_id
  AND cn.file_id = nb.source_file_id;

SELECT
    COUNT(*) AS total,
    COUNT(course_note_id) AS matched,
    COUNT(*) FILTER (
        WHERE course_note_id IS NULL
    ) AS unmatched
FROM note_block_test;

SELECT * from note_block_test;

ROLLBACK;