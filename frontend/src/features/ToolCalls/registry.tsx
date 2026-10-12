import type { ReactNode } from "react";
import { Flashcards } from "./components";
import LegacyLectureSources from "./components/legacy/LegacyLectureSources";
import { flashcardSetSchema } from "./schemas/practice";
import { legacySourceDocumentsSchema } from "./schemas/legacySources";

import { QuestionsPractice, multipleChoiceSetSchema } from "./MCQ";
import { WebSearchSources } from "./WebSearch/WebSearchSources";
import { webSearchSourcesSchema } from "./WebSearch/schema";

export type ToolEntry = {
  render: ToolRenderer;
  compact: boolean;
};
export type ToolRenderer = (data: unknown) => ReactNode;

const renderQuestions: ToolRenderer = (data) => {
  const result = multipleChoiceSetSchema.safeParse(data);
  return result.success ? (
    <QuestionsPractice data={result.data} />
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

const renderWebSearchSources: ToolRenderer = (data) => {
  const result = webSearchSourcesSchema.safeParse(data);
  return result.success ? (
    <WebSearchSources data={result.data} />
  ) : (
    <p role="alert">The search sources could not be displayed.</p>
  );
};

function createToolEntry(render: ToolRenderer, compact = false): ToolEntry {
  return { render, compact };
}

const questionsEntry = createToolEntry(renderQuestions);
const flashcardsEntry = createToolEntry(renderFlashcards);
const legacySourcesEntry = createToolEntry(renderLegacySources);
const webSearchEntry = createToolEntry(renderWebSearchSources, true);

// Artifact kinds take precedence; tool names remain supported as aliases.
export const toolCallRegistry: Readonly<Record<string, ToolEntry>> = {
  web_search: webSearchEntry,
  search: webSearchEntry,
  "multiple-choice-question": questionsEntry,
  create_multiple_choice_questions: questionsEntry,
  flashcards: flashcardsEntry,
  create_flashcards: flashcardsEntry,
  retrieval: legacySourcesEntry,
  legacy_lecture_sources: legacySourcesEntry,
};
