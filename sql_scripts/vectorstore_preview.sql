BEGIN;

SELECT
id, 
    collection_id,
    lgc.name as collection_name,
    LEFT(document, 100) AS document_preview,
    LEFT(lce.cmetadata::text, 10) AS metadata_preview
FROM langchain_pg_embedding AS lce
JOIN langchain_pg_collection AS lgc ON lgc.uuid = lce.collection_id;
JOIN note_block as nb ON nb.id=lgc.id
;

ROLLBACK;