import { useCallback, useState } from "react";

import { useAuth } from "../../Auth";
import {
  CoursesAPI,
  type Course,
  type CourseUpdate,
} from "../../../services/courses";

export function useEditCourse() {
  const { user } = useAuth();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const updateCourse = useCallback(
    async (courseId: string, data: CourseUpdate) => {
      if (!user) {
        throw new Error("You must be signed in to update a course.");
      }

      setLoading(true);
      setError(null);

      try {
        const token = await user.getIdToken();
        const updatedCourse = await CoursesAPI.updateCourse(
          token,
          courseId,
          data,
        );
        setCourse(updatedCourse);
        return updatedCourse;
      } catch (err) {
        const error =
          err instanceof Error ? err : new Error("Failed to update course.");
        setError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [user],
  );

  return { updateCourse, course, loading, error };
}
