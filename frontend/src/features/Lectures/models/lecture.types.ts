import { z } from "zod";

export type FileEntry = { path: string; url: string; parent?: string | null };
export type GroupedFiles = Record<string, FileEntry[]>;

export const PageRangeSchema = z.object({
  start_page: z.number(),
  end_page: z.number(),
});

export const QuestionTypeSchema = z.string();

export const OptionSchema = z.object({
  text: z.string(),
  is_correct: z.boolean(),
});

export const DerivationSchema = z.object({
  derivation_title: z.string(),
  derivation_stub: z.string(),
  steps: z.array(z.string()),
  reference: PageRangeSchema,
});

export const ExtractedQuestionSchema = z.object({
  question_text: z.string(),
  qtype: QuestionTypeSchema,
  topics: z.array(z.string()).default([]),
  options: z.array(OptionSchema).nullable().default(null),
  reference: PageRangeSchema.nullable().default(null),
  solution: z.array(z.string()).default([]),
});

export const ConceptualQuestionSchema = z.object({
  question: z.string(),
  topics: z.array(z.string()),
  options: z.array(OptionSchema),
  reference: PageRangeSchema,
  explanation: z.string(),
});

export const LectureAnalysisSchema = z.object({
  lecture_title: z.string(),
  lecture_summary: z.string(),
  core_topics: z.array(z.string()),
  learning_objectives: z.array(z.string()),
  assumed_prerequisites: z.array(z.string()).nullable().default(null),
  lecture_type: z.string().nullable().default(null),
});

export const LecturePayloadSchema = z.object({
  lecture_summary: LectureAnalysisSchema.nullable().optional(),
  lecture_analysis: LectureAnalysisSchema.nullable().optional(),
  derivations: z.array(DerivationSchema).default([]),
  extracted_questions: z.array(ExtractedQuestionSchema).default([]),
  conceptual_questions: z.array(ConceptualQuestionSchema).default([]),
});

export type PageRange = z.infer<typeof PageRangeSchema>;
export type QuestionType = z.infer<typeof QuestionTypeSchema>;
export type Option = z.infer<typeof OptionSchema>;
export type Derivation = z.infer<typeof DerivationSchema>;
export type ExtractedQuestion = z.infer<typeof ExtractedQuestionSchema>;
export type ConceptualQuestion = z.infer<typeof ConceptualQuestionSchema>;
export type LectureAnalysis = z.infer<typeof LectureAnalysisSchema>;
export type LecturePayload = z.infer<typeof LecturePayloadSchema>;

export type ParsedLecture = LecturePayload;
