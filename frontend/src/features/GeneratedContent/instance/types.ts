import type { MultipleChoiceQuestion } from "../../MCQ";

export type GeneratedContentState = {
  quizes: MultipleChoiceQuestion[];
};

export type GeneratedContentActions = {
  setQuizes: (token: string) => Promise<void>;
};

export type GeneratedContentStore = GeneratedContentState &
  GeneratedContentActions;
