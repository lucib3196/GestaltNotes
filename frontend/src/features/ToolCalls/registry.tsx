import type { ReactNode } from "react";
import { Flashcards, MultipleChoiceQuestions } from "./components";
import { flashcardSetSchema, multipleChoiceSetSchema } from "./schemas";

type ToolRenderer = (data: unknown) => ReactNode;

export const toolCallRegistry: Readonly<Record<string, ToolRenderer>> = {
  create_multiple_choice_questions: (data) => {
    const result = multipleChoiceSetSchema.safeParse(data);
    return result.success
      ? <MultipleChoiceQuestions data={result.data} />
      : <p role="alert">The question data could not be displayed.</p>;
  },
  create_flashcards: (data) => {
    const result = flashcardSetSchema.safeParse(data);
    return result.success
      ? <Flashcards data={result.data} />
      : <p role="alert">The flashcard data could not be displayed.</p>;
  },
};
