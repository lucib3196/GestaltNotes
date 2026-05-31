import { createStore } from "zustand";
import type { LectureState, LectureStore } from "./types";

const initialState: LectureState = {
  selectedFile: null,
  files: [],
};

export function createLectureStore(preloaded?: Partial<LectureState>) {
  return createStore<LectureStore>()((set) => ({
    ...preloaded,
    ...initialState,
    setSelectedFile: (file) => set({ selectedFile: file }),
    setFiles: (files) => set({ files: files }),
  }));
}
