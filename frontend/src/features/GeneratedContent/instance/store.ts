import { createStore } from "zustand";
import type { GeneratedContentState, GeneratedContentStore } from "./types";
import { MCQClient } from "../../MCQ";

const initialState: GeneratedContentState = {
  quizes: [],
};

export function createGenContentStore(
  preloaded?: Partial<GeneratedContentState>,
) {
  return createStore<GeneratedContentStore>()((set) => ({
    ...preloaded,
    ...initialState,
    setQuizes: async (token) => {
      try {
        const quizes = await MCQClient.getAllQuizzes(token);
        set(() => ({ quizes: quizes }));
      } catch {}
    },
  }));
}
