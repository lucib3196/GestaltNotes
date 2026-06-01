import { useAuth } from "../../../context";
import type { ThreadCreate } from "../../../services";
import { ChatAPI } from "../../../services";
import { useThreadStore } from "../instance/store";
import { useState, useCallback, useEffect } from "react";
import type { ThreadUpdate } from "../../../services/chat/types";


export const useGenerateThread = () => {
  const { user } = useAuth();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
      const setThread = useThreadStore((s) => s.setThread);
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
  const threadId = useThreadStore((s) => s.threadId);
  const setThread = useThreadStore((s) => s.setThread);

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

export const useGetThreads = () => {
  const { user } = useAuth();

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);

  const setThreads = useThreadStore((s) => s.setThreads);

  const getThreads = useCallback(async () => {
    if (!user) {
      setError("User not authenticated");

      return;
    }

    setLoading(true);
    setError(null);

    try {
      const token = await user.getIdToken();

      const threads = await ChatAPI.listMyThreads(token);

      setThreads(threads);
    } catch (error) {
      setError(`Error getting threads: ${String(error)}`);
    } finally {
      setLoading(false);
    }
  }, [user, setThreads]);

  return {
    getThreads,
    loading,
    error,
  };
};

export function useUpdateThread() {
  const { user } = useAuth();

  const updateThreadInStore = useThreadStore((s) => s.updateThread);

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
