import { useCallback, useEffect, useState } from "react";

import { useAuth } from "../../Auth";
import { CoursesAPI, type Course } from "../../../services/courses";

export function useFetchMyCourses() {
  const { user } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchCourses = useCallback(async () => {
    if (!user) {
      setCourses([]);
      return [];
    }

    setLoading(true);
    setError(null);

    try {
      const token = await user.getIdToken();
      const ownedCourses = await CoursesAPI.listOwnedCourses(token);
      setCourses(ownedCourses);
      return ownedCourses;
    } catch (err) {
      const error =
        err instanceof Error ? err : new Error("Failed to fetch courses.");
      setError(error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    void fetchCourses();
  }, [fetchCourses]);

  return { courses, loading, error, refetch: fetchCourses };
}
