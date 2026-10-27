import { createContext } from "react";
import type { createCourseDetailsStore } from "./store";

export const CourseDetailsContext = createContext<
  ReturnType<typeof createCourseDetailsStore> | null
>(null);
