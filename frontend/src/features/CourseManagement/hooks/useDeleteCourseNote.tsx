import { useCallback, useState } from "react";

import { useAuth } from "../../Auth";
import { CoursesAPI, type CourseNoteDelete } from "../../../services/courses";

export function useDeleteCourseNote() {
  const { user } = useAuth();
  const [result, setResult] = useState<CourseNoteDelete | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const deleteCourseNote = useCallback(
    async (courseId: string, noteId: string) => {
      if (!user) {
        throw new Error("You must be signed in to remove notes.");
      }

      setLoading(true);
      setError(null);

      try {
        const token = await user.getIdToken();
        const deletedNote = await CoursesAPI.deleteCourseNote(
          token,
          courseId,
          noteId,
        );
        setResult(deletedNote);
        return deletedNote;
      } catch (err) {
        const error =
          err instanceof Error ? err : new Error("Failed to remove note.");
        setError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [user],
  );

  return { deleteCourseNote, result, loading, error };
}
