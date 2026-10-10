import type { ReactNode } from "react";
import { Flashcards, MultipleChoiceQuestions } from "./components";
import LegacyLectureSources from "./components/legacy/LegacyLectureSources";
import {
  flashcardSetSchema,
  multipleChoiceSetSchema,
} from "./schemas/practice";
import { legacySourceDocumentsSchema } from "./schemas/legacySources";

type ToolRenderer = (data: unknown) => ReactNode;

const renderQuestions: ToolRenderer = (data) => {
  const result = multipleChoiceSetSchema.safeParse(data);
  return result.success ? (
    <MultipleChoiceQuestions data={result.data} />
  ) : (
    <p role="alert">The question data could not be displayed.</p>
  );
};
const renderFlashcards: ToolRenderer = (data) => {
  const result = flashcardSetSchema.safeParse(data);
  return result.success ? (
    <Flashcards data={result.data} />
  ) : (
    <p role="alert">The flashcard data could not be displayed.</p>
  );
};
const renderLegacySources: ToolRenderer = (data) => {
  const result = legacySourceDocumentsSchema.safeParse(data);
  return result.success ? (
    <LegacyLectureSources data={result.data} />
  ) : (
    <p role="alert">The lecture source data could not be displayed.</p>
  );
};

// Artifact kinds take precedence; tool names remain supported as aliases.
export const toolCallRegistry: Readonly<Record<string, ToolRenderer>> = {
  "multiple-choice-question": renderQuestions,
  create_multiple_choice_questions: renderQuestions,
  flashcards: renderFlashcards,
  create_flashcards: renderFlashcards,
  retrieval: renderLegacySources,
  legacy_lecture_sources: renderLegacySources,
};
