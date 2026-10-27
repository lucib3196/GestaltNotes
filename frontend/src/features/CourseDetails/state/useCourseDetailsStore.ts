import { useContext } from "react";
import { useStore } from "zustand";
import type { CourseDetailsStore } from "./store";
import { CourseDetailsContext } from "./context";

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
