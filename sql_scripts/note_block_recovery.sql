BEGIN;



UPDATE note_block as nb
SET
-- Get the first non null value and set the course id to it
    course_id =  COALESCE(
        nb.course_id, 
        (lce.cmetadata->>'course_id')::uuid
    ),
    source_file_id = COALESCE(
        nb.source_file_id, (lce.cmetadata->>'source_file_id')::uuid
    )
FROM langchain_pg_embedding AS lce
WHERE lce.id = nb.id::text AND (
    nb.course_id is null
    or nb.source_file_id is NULL
);
-- RETURNING nb.id, nb.title, nb.course_id, nb.source_file_id;

SELECT
    COUNT(*) AS total_blocks,
    COUNT(course_id) AS with_course,
    COUNT(source_file_id) AS with_source_file,
    COUNT(*) FILTER (
        WHERE course_id IS NULL OR source_file_id IS NULL
    ) AS still_missing
FROM note_block;

-- ROLLBACK;
COMMIT;