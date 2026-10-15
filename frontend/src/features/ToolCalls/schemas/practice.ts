import { z } from "zod";

export { mcqQuestion, multipleChoiceSetSchema } from "../MCQ/schema";
export type { MultipleChoiceSet, MCQQuestion } from "../MCQ/types";

export const flashcardSetSchema = z.object({
  cards: z
    .array(
      z.object({
        front: z.string().min(1),
        back: z.string().min(1),
      }),
    )
    .min(1),
});
export type FlashcardSet = z.infer<typeof flashcardSetSchema>;
