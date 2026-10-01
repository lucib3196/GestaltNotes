import { useCallback, useState } from "react";

import { useAuth } from "../../Auth";
import { CoursesAPI } from "../../../services/courses";

export function useStreamCourseNote() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const streamCourseNote = useCallback(
    async (courseId: string, noteId: string) => {
      if (!user) {
        throw new Error("You must be signed in to view notes.");
      }

      setLoading(true);
      setError(null);

      try {
        const token = await user.getIdToken();
        const blob = await CoursesAPI.streamCourseNote(token, courseId, noteId);
        const url = URL.createObjectURL(blob);
        console.log("URL for image",url)
        window.open(url, "_blank", "noopener,noreferrer");
        return url;
      } catch (err) {
        const error =
          err instanceof Error ? err : new Error("Failed to open note.");
        setError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [user],
  );

  return { streamCourseNote, loading, error };
}
