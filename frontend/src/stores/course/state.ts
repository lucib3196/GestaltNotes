import type { Course, CourseNoteOverview } from "../../services/courses";

export type CourseState = {
  selectedCourseId: string;
  selectedCourse: Course | null;
};

export type CourseActions = {
  setSelectedCourseId: (id: string) => void;
  setSelectedCourse: (course: Course | null) => void;
};

export type CourseNotesState = {
  notesById: Record<string, CourseNoteOverview>;

  selectedNoteID: string | null;
  checkedNoteIds: string[];

  notesLoading: boolean;
  notesError: string | null;
};

export type CourseNoteActions = {
  setNotes: (notes: CourseNoteOverview[]) => void;
  
  removeNotes: (ids: string[]) => void;

  selectNote: (id: string | null) => void;
  getSelectedNote: () => CourseNoteOverview | null;
  toggleCheckedNote: (id: string) => void;
  clearCheckedNotes: () => void;

  setNotesLoading: (loading: boolean) => void;
  setNotesError: (error: string | null) => void;
};
export type CourseStore = CourseState & CourseActions;
export type CourseNoteStore = CourseNotesState & CourseNoteActions
