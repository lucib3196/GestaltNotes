import { useAuth } from "../../Auth";
import { useState } from "react";
import type { ThreadCreate } from "../../../services";
import { ChatAPI } from "../../../services";
import type { Thread } from "../../../services";

export const useCreateThread = () => {
  const { user } = useAuth();
  const [thread, setThread] = useState<Thread | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createThread = async (data: ThreadCreate): Promise<Thread> => {
    setError(null);
    if (!user) {
      const message = "User not authenticated";
      setError(message);
      throw new Error(message);
    }

    setLoading(true);

    try {
      const token = await user.getIdToken();
      const createdThread = await ChatAPI.createThread(data, token);
      setThread(createdThread);
      return createdThread;
    } catch (error) {
      setError(`Error creating thread: ${String(error)}`);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return { thread, loading, error, createThread };
};
