import { createStore } from "zustand/vanilla";
import {
  createCourseStore,
  createCourseNoteStore,
} from "../../../stores/course/slice";
import { type CourseNoteStore } from "../../../stores/course/state";
import type { CourseStore } from "../../../stores/course/state";
import {
  createCourseFileSlice,
  type CourseFileStore,
} from "../../../stores/courseFiles";

export type CourseDetailsStore = CourseStore &
  CourseFileStore &
  CourseNoteStore;

export function createCourseDetailsStore(courseId: string) {
  return createStore<CourseDetailsStore>()((...args) => ({
    ...createCourseNoteStore()(...args),
    ...createCourseStore<CourseDetailsStore>()(...args),
    ...createCourseFileSlice<CourseDetailsStore>()(...args),
    selectedCourseId: courseId,
  }));
}
