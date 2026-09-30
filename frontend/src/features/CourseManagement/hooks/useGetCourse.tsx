import { useCallback, useEffect, useState } from "react";

import { useAuth } from "../../Auth";
import { CoursesAPI, type Course } from "../../../services/courses";

export function useGetCourse(courseId: string | undefined) {
  const { user } = useAuth();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchCourse = useCallback(async () => {
    if (!user || !courseId) {
      setCourse(null);
      return null;
    }

    setLoading(true);
    setError(null);

    try {
      const token = await user.getIdToken();
      const courseData = await CoursesAPI.getCourse(token, courseId);
      setCourse(courseData);
      return courseData;
    } catch (err) {
      const error =
        err instanceof Error ? err : new Error("Failed to fetch course.");
      setError(error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [user, courseId]);

  useEffect(() => {
    void fetchCourse();
  }, [fetchCourse]);

  return { course, loading, error, refetch: fetchCourse };
}
