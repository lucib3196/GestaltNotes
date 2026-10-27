import { useCallback, useEffect, useRef, useState } from "react";

import { useAuth } from "../../features/Auth";
import { CoursesAPI, type Course } from "../../services/courses";

export function useGetCourse(courseId: string | undefined) {
  const { user } = useAuth();
  const requestId = useRef(0);
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchCourse = useCallback(async () => {
    const request = ++requestId.current;
    if (!user || !courseId) {
      setCourse(null);
      setLoading(false);
      return null;
    }

    setLoading(true);
    setError(null);

    try {
      const token = await user.getIdToken();
      const courseData = await CoursesAPI.getCourse(token, courseId);
      if (request === requestId.current) setCourse(courseData);
      return courseData;
    } catch (err) {
      const error =
        err instanceof Error ? err : new Error("Failed to fetch course.");
      if (request === requestId.current) setError(error);
      throw error;
    } finally {
      if (request === requestId.current) setLoading(false);
    }
  }, [user, courseId]);

  useEffect(() => {
    let active = true;
    queueMicrotask(() => {
      if (active) void fetchCourse().catch(() => {
        // The caller displays the fetch error.
      });
    });
    return () => {
      active = false;
      requestId.current += 1;
    };
  }, [fetchCourse]);

  return { course, loading, error, refetch: fetchCourse };
}
