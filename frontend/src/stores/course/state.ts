import type { Course } from "../../services/courses";

export type CourseState = {
  selectedCourseId: string;
  selectedCourse: Course | null;
};

export type CourseActions = {
  setSelectedCourseId: (id: string) => void;
  setSelectedCourse: (course: Course | null) => void;
};

export type CourseStore = CourseState & CourseActions;
