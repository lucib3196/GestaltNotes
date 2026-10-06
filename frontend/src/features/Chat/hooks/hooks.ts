import { useAuth } from "../../Auth";
import type { ThreadCreate } from "../../../services";
import { ChatAPI } from "../../../services";

import { useState, useCallback, useEffect } from "react";
import type { ThreadUpdate } from "../../../services/chat/types";


export const useGenerateThread = () => {
  const { user } = useAuth();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const setThread = useChatStore((s) => s.setThread);

  const generateThread = async (data: ThreadCreate) => {
    setLoading(true);
    setError(null);
    if (!user) {
      setError("User not authenticated");
      return;
    }

    try {
      const token = await user?.getIdToken();
      const thread = await ChatAPI.createThread(data, token);
      setThread(thread);
    } catch (error) {
      let errMsg = `Error generating thread: ${error}`;
      setError(errMsg);
    } finally {
      setLoading(false);
    }
  };

  return { loading, generateThread, error };
};

export const useGetThread = () => {
  const { user } = useAuth();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const threadId = useChatStore((s) => s.threadId);
  const setThread = useChatStore((s) => s.setThread);

  useEffect(() => {
    if (!user || !threadId) return;

    let cancelled = false;

    const load = async () => {
      try {
        setLoading(true);

        const token = await user.getIdToken();

        const thread = await ChatAPI.getThread(threadId, token);

        if (!cancelled) {
          setThread(thread);
        }
      } catch (error) {
        if (!cancelled) {
          setError(String(error));
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    load();

    return () => {
      cancelled = true;
    };
  }, [user, threadId, setThread]);

  return {
    loading,
    error,
  };
};



export function useUpdateThread() {
  const { user } = useAuth();

  const updateThreadInStore = useChatStore((s) => s.updateThread);

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

        updateThreadInStore(updatedThread);

        return updatedThread;
      } catch (error) {
        setError(`Failed to update thread: ${String(error)}`);

        throw error;
      } finally {
        setLoading(false);
      }
    },
    [user, updateThreadInStore],
  );

  return {
    updateThread,
    loading,
    error,
  };
}
