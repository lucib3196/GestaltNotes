import { z } from "zod";

// Metadata emitted by the existing lecture-ingestion pipeline.
export const legacySourceMetadataSchema = z.object({
  course: z.string().optional(),
  lecture_title: z.string().optional(),
  source_pdf: z.string().optional(),
  source_markdown: z.string().optional(),
}).catchall(z.unknown());

export const legacySourceDocumentSchema = z.object({
  id: z.string().optional(),
  page_content: z.string(),
  metadata: legacySourceMetadataSchema,
});

export const legacySourceDocumentsSchema = z.array(legacySourceDocumentSchema);
export type LegacySourceDocumentSet = z.infer<typeof legacySourceDocumentsSchema>;
