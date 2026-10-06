import { useAuth } from "../../Auth";
import { useEffect, useState } from "react";
import type { Thread } from "../../../services";
import { ChatAPI } from "../../../services";
export const useGetThreads = () => {
  const { user } = useAuth();
  const [thread, setThreads] = useState<Thread[]>([]);

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
  }, [user]);

  return {
    loading,
    error,
  };
};
