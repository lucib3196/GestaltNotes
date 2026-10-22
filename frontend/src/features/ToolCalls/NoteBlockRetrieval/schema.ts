import { z } from "zod";

export const SourceMetadataSchemaV1 = z.object({
  note_block_id: z.string().uuid(),
  title: z.string(),
  kind: z.string(),
  position: z.number().int(),
  revision: z.number().int(),
  schema_version: z.literal(1),

  course_id: z.string().uuid().nullish(),
  course_name: z.string().nullish(),

  source_file_id: z.string().uuid().nullish(),
  filename: z.string().nullish(),
  storage_key: z.string().nullish(),
  content_type: z.string().nullish(),
  download_url: z.string().nullish(),

  page_start: z.number().int().nullish(),
  page_end: z.number().int().nullish(),
}).catchall(z.unknown());

export type SourceMetadataV1 = z.infer<typeof SourceMetadataSchemaV1>;

export const noteBlockDocumentSchema = z.object({
  id: z.string().nullish(),
  page_content: z.string(),
  metadata: SourceMetadataSchemaV1,
});

export const noteBlockDocumentsSchema = z.array(noteBlockDocumentSchema);
export type NoteBlockDocuments = z.infer<typeof noteBlockDocumentsSchema>;
