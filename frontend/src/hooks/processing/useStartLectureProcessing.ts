import { useCallback, useState } from "react";
import { useAuth } from "../../features/Auth";
import {
  ProcessingTasksAPI,
  type ProcessingTaskStarted,
} from "../../services/processing";

export function useStartLectureProcessing() {
  const { user } = useAuth();
  const [task, setTask] = useState<ProcessingTaskStarted | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const startProcessing = useCallback(
    async (courseId: string, noteId: string) => {
      setLoading(true);
      setError(null);
      setTask(null);

      try {
        if (!user) {
          throw new Error("You must be signed in to process materials.");
        }

        const token = await user.getIdToken();
        const started = await ProcessingTasksAPI.startLecture(
          token,
          courseId,
          noteId,
        );
        setTask(started);
        return started;
      } catch (cause) {
        const failure =
          cause instanceof Error
            ? cause
            : new Error("Failed to start processing.");
        setError(failure);
        throw failure;
      } finally {
        setLoading(false);
      }
    },
    [user],
  );

  return { startProcessing, task, loading, error };
}
