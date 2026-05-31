import { useAuth } from "../../../context";
import { UseLectureChatContext } from "../../../context/ChatContext";
import type { ThreadCreate } from "../../../services";
import { api } from "../../../config";
import { ChatAPI } from "../../../services";
import { useThreadStore } from "../instance/store";
import { useState, useCallback } from "react";
import type { ThreadUpdate } from "../../../services/chat/types";
type Thread = {
  id: string;
  user_id: string;
  title: string | null;
  agent: string | null;
  created_at: string;
  updated_at: string;
};

export const useGenerateThread = () => {
  const { user } = useAuth();
  const { setThreadId } = UseLectureChatContext();

  const generateThread = async (data: ThreadCreate): Promise<Thread> => {
    const token = await user?.getIdToken();

    try {
      const response = await api.post<Thread>("/users/thread/", data, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.data.id) {
        throw new Error("Failed to generate thread id");
      }

      setThreadId(response.data.id);

      return response.data;
    } catch (error) {
      console.error("Error generating thread:", error);
      throw error;
    }
  };

  return generateThread;
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
