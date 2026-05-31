import type { FileEntry } from "../models/lecture.types";

export type LectureState = {
  selectedFile: FileEntry | null;
  files: FileEntry[];
};

export type LectureActions = {
  setSelectedFile: (file: FileEntry) => void;
  setFiles: (files: FileEntry[]) => void;
};

export type LectureStore = LectureActions & LectureState;
