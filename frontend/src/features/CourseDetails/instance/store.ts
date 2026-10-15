import { createStore } from "zustand/vanilla";
import { createCourseStore } from "../../../stores/course/slice";
import type { CourseStore } from "../../../stores/course/state";
import {
  createCourseFileSlice,
  type CourseFileStore,
} from "../../../stores/courseFiles";

export type CourseDetailsStore = CourseStore & CourseFileStore;

export function createCourseDetailsStore(courseId: string) {
  return createStore<CourseDetailsStore>()((...args) => ({
    ...createCourseStore<CourseDetailsStore>()(...args),
    ...createCourseFileSlice<CourseDetailsStore>()(...args),
    selectedCourseId: courseId,
  }));
}
