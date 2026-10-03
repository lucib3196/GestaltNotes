import { useCallback, useState } from "react";

import { useAuth } from "../../Auth";
import {
  CoursesAPI,
  type Course,
  type CourseCreate,
} from "../../../services/courses";

export function useCreateCourse() {
  const { user } = useAuth();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const createCourse = useCallback(
    async (data: CourseCreate) => {
      if (!user) {
        throw new Error("You must be signed in to create a course.");
      }

      setLoading(true);
      setError(null);

      try {
        const token = await user.getIdToken();
        const createdCourse = await CoursesAPI.createCourse(token, data);
        setCourse(createdCourse);
        return createdCourse;
      } catch (err) {
        const error =
          err instanceof Error ? err : new Error("Failed to create course.");
        setError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [user],
  );

  return { createCourse, course, loading, error };
}
