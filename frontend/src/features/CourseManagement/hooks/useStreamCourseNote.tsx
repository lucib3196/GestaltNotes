import { useCallback, useEffect, useRef, useState } from "react";
import { useAuth } from "../../Auth";
import { CoursesAPI } from "../../../services/courses";

export function useStreamCourseNote() {
  const { user } = useAuth();
  const activeRequest = useRef<AbortController | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const cancel = useCallback(() => {
    activeRequest.current?.abort();
    activeRequest.current = null;
    setLoading(false);
    setError(null);
  }, []);

  useEffect(() => () => {
    activeRequest.current?.abort();
    activeRequest.current = null;
  }, [user]);

  const streamCourseNote = useCallback(
    async (courseId: string, noteId: string): Promise<Blob | null> => {
      activeRequest.current?.abort();
      const controller = new AbortController();
      activeRequest.current = controller;
      setLoading(true);
      setError(null);

      try {
        if (!user) throw new Error("You must be signed in to view notes.");
        const token = await user.getIdToken();
        if (controller.signal.aborted) return null;
        const blob = await CoursesAPI.streamCourseNote(
          token, courseId, noteId, controller.signal,
        );
        return controller.signal.aborted ? null : blob;
      } catch (err) {
        if (controller.signal.aborted) return null;
        const failure = err instanceof Error ? err : new Error("Failed to open note.");
        if (activeRequest.current === controller) setError(failure);
        throw failure;
      } finally {
        if (activeRequest.current === controller) {
          activeRequest.current = null;
          setLoading(false);
        }
      }
    },
    [user],
  );

  return { streamCourseNote, cancel, loading, error };
}
