import { useAuth } from "../../Auth";
import { ChatAPI } from "../../../services";

import { useState, useCallback} from "react";
import type { ThreadUpdate } from "../../../services/chat/types";

export function useUpdateThread() {
  const { user } = useAuth();

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);

  const updateThread = useCallback(
    async (threadId: string, update: ThreadUpdate) => {
      if (!user) {
        setError("User not authenticated");
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const token = await user.getIdToken();

        const updatedThread = await ChatAPI.updateThread(
          threadId,
          update,
          token,
        );

        // updateThreadInStore(updatedThread);

        return updatedThread;
      } catch (error) {
        setError(`Failed to update thread: ${String(error)}`);

        throw error;
      } finally {
        setLoading(false);
      }
    },
    [user],
  );

  return {
    updateThread,
    loading,
    error,
  };
}
