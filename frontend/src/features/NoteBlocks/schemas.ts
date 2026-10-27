import { z } from "zod";

export const pageRangeSchema = z.object({
  start: z.number().int().nonnegative(),
  end: z.number().int().nonnegative(),
}).refine((range) => range.end >= range.start, {
  message: "The last page must not precede the first page.",
});

export const optionSchema = z.object({
  label: z.string().nullable(),
  text: z.string(),
  is_correct: z.boolean().nullable(),
});

export const lectureSummarySchema = z.object({
  title: z.string(),
  summary: z.string(),
  topics: z.array(z.string()),
  objectives: z.array(z.string()),
  prerequisites: z.array(z.string()),
  kind: z.enum(["conceptual", "derivation", "computational", "mixed"]),
});

export const solutionStepSchema = z.object({
  explanation: z.string(),
  equation: z.string().nullable(),
  reference: pageRangeSchema.nullable(),
});

export const extractedQuestionSchema = z.object({
  question: z.string(),
  kind: z.enum([
    "conceptual", "computational", "derivation", "multiple_choice",
    "short_answer", "mixed",
  ]),
  topics: z.array(z.string()),
  options: z.array(optionSchema),
  solution: z.array(solutionStepSchema),
  answer: z.string().nullable(),
  gaps: z.array(z.string()),
  reference: pageRangeSchema.nullable(),
});

export const derivationStepSchema = z.object({
  equation_latex: z.string().nullable(),
  explanation: z.string(),
  rule_used: z.string().nullable(),
  reference: pageRangeSchema,
});

export const derivationSchema = z.object({
  title: z.string(),
  description: z.string(),
  assumptions: z.array(z.string()),
  symbols: z.array(z.object({ symbol: z.string(), meaning: z.string() })),
  steps: z.array(derivationStepSchema),
  result_latex: z.string().nullable(),
  completeness: z.enum(["complete", "partial", "unclear"]),
  gaps: z.array(z.string()),
  reference: pageRangeSchema,
});

export const conceptualQuestionSchema = z.object({
  question: z.string(),
  topics: z.array(z.string()),
  options: z.array(optionSchema),
  answer: z.string().nullable(),
  explanation: z.string().nullable(),
  reference: pageRangeSchema.nullable(),
});

// Validate the envelope separately so unsupported content can have a fallback.
export const noteBlockSchema = z.object({
  id: z.string().uuid(),
  course_id: z.string().uuid().nullable(),
  source_file_id: z.string().uuid().nullable(),
  title: z.string(),
  kind: z.string().nullable(),
  content: z.record(z.string(), z.unknown()),
  position: z.number().int().nonnegative(),
  page_start: z.number().int().nonnegative().nullable(),
  page_end: z.number().int().nonnegative().nullable(),
  revision: z.number().int().nonnegative(),
  schema_version: z.number().int().positive(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type PageRange = z.infer<typeof pageRangeSchema>;
export type SourceOption = z.infer<typeof optionSchema>;
export type LectureSummaryContent = z.infer<typeof lectureSummarySchema>;
export type ExtractedQuestionContent = z.infer<typeof extractedQuestionSchema>;
export type DerivationContent = z.infer<typeof derivationSchema>;
export type ConceptualQuestionContent = z.infer<typeof conceptualQuestionSchema>;
export type NoteBlock = z.infer<typeof noteBlockSchema>;
export type NoteBlockKind =
  | "lecture_summary"
  | "extracted_question"
  | "derivation"
  | "conceptual_question";
