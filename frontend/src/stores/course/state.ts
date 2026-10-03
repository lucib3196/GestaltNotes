import type { Course } from "../../services/courses";

export type CourseState = {
  selectedCourseId: string;
  selectedCourse: Course|null;
  courseById: Record<string, Course>;
};

export type CourseActions = {
  setSelectedCourseId: (id: string) => void;
  setCoursesById: (courses: Course[]) => void;

};

export type CourseStore = CourseState & CourseActions;
