import { z } from "zod";

export const multipleChoiceSetSchema = z.object({
  questions: z.array(z.object({
    question: z.string().min(1),
    options: z.array(z.string().min(1)).length(4),
    correct_answer_index: z.number().int().min(0).max(3),
    explanation: z.string().min(1),
  })).min(1),
});

export const flashcardSetSchema = z.object({
  cards: z.array(z.object({
    front: z.string().min(1),
    back: z.string().min(1),
  })).min(1),
});

export type MultipleChoiceSet = z.infer<typeof multipleChoiceSetSchema>;
export type FlashcardSet = z.infer<typeof flashcardSetSchema>;
