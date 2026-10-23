import { useState, type ReactNode } from "react";
import { createCourseDetailsStore } from "./store";
import { CourseDetailsContext } from "./context";

export function CourseDetailsProvider({
  courseId,
  children,
}: {
  courseId: string;
  children: ReactNode;
}) {
  const [store] = useState(() => createCourseDetailsStore(courseId));

  return (
    <CourseDetailsContext.Provider value={store}>
      {children}
    </CourseDetailsContext.Provider>
  );
}
