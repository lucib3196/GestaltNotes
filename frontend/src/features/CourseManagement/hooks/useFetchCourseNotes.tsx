import { useCallback, useEffect, useState } from "react";

import { useAuth } from "../../Auth";
import { CoursesAPI, type CourseNote } from "../../../services/courses";

export function useFetchCourseNotes(courseId: string | undefined) {
  const { user } = useAuth();
  const [notes, setNotes] = useState<CourseNote[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchNotes = useCallback(async () => {
    if (!user || !courseId) {
      setNotes([]);
      return [];
    }

    setLoading(true);
    setError(null);

    try {
      const token = await user.getIdToken();
      const courseNotes = await CoursesAPI.listCourseNotes(token, courseId);
      setNotes(courseNotes);
      return courseNotes;
    } catch (err) {
      const error =
        err instanceof Error ? err : new Error("Failed to fetch course notes.");
      setError(error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [user, courseId]);

  useEffect(() => {
    let active = true;
    queueMicrotask(() => {
      if (active) void fetchNotes().catch(() => {
        // The hook exposes fetch errors to the resource list.
      });
    });
    return () => { active = false; };
  }, [fetchNotes]);

  return { notes, loading, error, refetch: fetchNotes };
}
