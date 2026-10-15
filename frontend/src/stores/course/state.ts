import type { Course } from "../../services/courses";

export type CourseState = {
  selectedCourseId: string;
  selectedCourse: Course | null;
};

export type CourseActions = {
  setSelectedCourseId: (id: string) => void;
};

export type CourseStore = CourseState & CourseActions;
