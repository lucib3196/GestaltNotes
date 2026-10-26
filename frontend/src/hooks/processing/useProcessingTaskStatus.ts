import { useCallback, useState } from "react";
import { useAuth } from "../../features/Auth";
import {
  ProcessingTasksAPI,
  type ProcessingTaskStatus,
} from "../../services/processing";

export function useProcessingTaskStatus() {
  const { user } = useAuth();
  const [taskStatus, setTaskStatus] =
    useState<ProcessingTaskStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const checkStatus = useCallback(
    async (taskId: string) => {
      setLoading(true);
      setError(null);

      try {
        if (!user) {
          throw new Error("You must be signed in to check processing.");
        }

        const token = await user.getIdToken();
        const status = await ProcessingTasksAPI.getTaskStatus(token, taskId);
        setTaskStatus(status);
        return status;
      } catch (cause) {
        const failure =
          cause instanceof Error
            ? cause
            : new Error("Failed to check processing status.");
        setError(failure);
        throw failure;
      } finally {
        setLoading(false);
      }
    },
    [user],
  );

  return { checkStatus, taskStatus, loading, error };
}
