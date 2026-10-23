import { useCallback, useEffect, useRef, useState } from "react";

import { useAuth } from "../../features/Auth";
import { CoursesAPI, type Course } from "../../services/courses";

export function useFetchMyCourses(enabled = true) {
  const { user } = useAuth();
  const requestId = useRef(0);
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchCourses = useCallback(async () => {
    const request = ++requestId.current;
    if (!user || !enabled) {
      setCourses([]);
      setLoading(false);
      setError(null);
      return [];
    }

    setLoading(true);
    setError(null);

    try {
      const token = await user.getIdToken();
      const ownedCourses = await CoursesAPI.listOwnedCourses(token);
      if (request === requestId.current) setCourses(ownedCourses);
      return ownedCourses;
    } catch (err) {
      const error =
        err instanceof Error ? err : new Error("Failed to fetch courses.");
      if (request === requestId.current) setError(error);
      throw error;
    } finally {
      if (request === requestId.current) setLoading(false);
    }
  }, [user, enabled]);

  useEffect(() => {
    let active = true;
    queueMicrotask(() => {
      if (active) void fetchCourses().catch(() => {
        // The caller displays the fetch error.
      });
    });
    return () => {
      active = false;
      requestId.current += 1;
    };
  }, [fetchCourses]);

  return { courses, loading, error, refetch: fetchCourses };
}
