import { useAuth } from "../../Auth";
import { ChatAPI } from "../../../services";

import { useState, useEffect } from "react";

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

