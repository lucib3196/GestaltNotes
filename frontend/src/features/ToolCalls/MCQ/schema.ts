import { z } from "zod";

export const mcqQuestion = z.object({
  question: z.string().min(1),
  options: z.array(z.string().min(1)).length(4),
  correct_answer_index: z.number().int().min(0).max(3),
  explanation: z.string().min(1),
});

export const multipleChoiceSetSchema = z.object({
  quiz_title: z.string().min(1).optional(),
  description: z.string().min(1).optional(),
  questions: z.array(mcqQuestion).min(1),
});
