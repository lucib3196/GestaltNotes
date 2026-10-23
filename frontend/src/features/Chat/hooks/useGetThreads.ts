import { useAuth } from "../../Auth";
import { useEffect, useState, useCallback, useMemo } from "react";
import type { Thread } from "../../../services";
import { useChatStore } from "../instance";
import { ChatAPI } from "../../../services";

export const useGetThreads = () => {
  const { user } = useAuth();
  const setThreads = useChatStore((state) => state.setThreads);
  const threadIds = useChatStore((state) => state.threadIds);
  const threadsById = useChatStore((state) => state.threadsById);
  const threads = useMemo(() => threadIds.map((id) => threadsById[id]).filter((thread): thread is Thread => Boolean(thread)), [threadIds, threadsById]);
  const [refreshKey, setRefreshKey] = useState(0);
  const refetch = useCallback(() => {
    setRefreshKey((key) => key + 1);
  }, []);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const getThreads = async () => {
      if (!user) {
        setError("User not authenticated");

        return;
      }

      setLoading(true);
      setError(null);

      try {
        const token = await user.getIdToken();

        const results = await ChatAPI.listMyThreads(token);
        if (active) setThreads(results);
      } catch (error) {
        if (active) setError(`Error getting threads: ${String(error)}`);
      } finally {
        if (active) setLoading(false);
      }
    };
    void getThreads();
    return () => {
      active = false;
    };
  }, [user, refreshKey, setThreads]);

  return {
    threads,
    loading,
    error,
    refetch,
  };
};
