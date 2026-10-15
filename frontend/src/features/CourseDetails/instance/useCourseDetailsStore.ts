import { createContext, useContext } from "react";
import { useStore } from "zustand";
import type { createCourseDetailsStore, CourseDetailsStore } from "./store";

export const CourseDetailsContext = createContext<
  ReturnType<typeof createCourseDetailsStore> | null
>(null);

export function useCourseDetailsStore<T>(
  selector: (state: CourseDetailsStore) => T,
): T {
  const store = useContext(CourseDetailsContext);
  if (!store) {
    throw new Error(
      "useCourseDetailsStore requires CourseDetailsProvider",
    );
  }
  return useStore(store, selector);
}
