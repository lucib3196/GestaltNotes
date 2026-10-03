import type { StateCreator } from "zustand";
import type { CourseStore } from "./state";
import type { Course } from "../../services/courses";

export type CourseSliceCreator<
  Store extends CourseStore = CourseStore,
  Slice = CourseStore,
> = StateCreator<Store, [], [], Slice>;

export function coursesById(courses: Course[]): Record<string, Course> {
  const byId: Record<string, Course> = {};
  for (const c of courses) {
    if (!c.id) continue;
    byId[c.id] = c;
  }
  return byId;
}

export function createCourseStore<
  Store extends CourseStore = CourseStore,
>(): CourseSliceCreator<Store, CourseStore> {
  return (set) => ({
    selectedCourseId: "",
    courseById: {},
    selectedCourse: null,
    setSelectedCourseId: (id) => {
      set(
        (state) =>
          ({
            selectedCourse: state.courseById[id],
            selectedCourseId: id,
          }) as Partial<Store>,
      );
    },
    setCoursesById: (courses) => {
      set(() => {
        return { courseById: coursesById(courses) } as Partial<Store>;
      });
    },
  });
}
