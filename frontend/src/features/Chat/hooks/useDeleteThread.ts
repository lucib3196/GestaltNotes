import { useCallback, useRef, useState } from "react";
import { useAuth } from "../../Auth";
import { ChatAPI } from "../../../services";

export function useDeleteThread() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const pending = useRef(false);

  const deleteThread = useCallback(async (threadId: string): Promise<void> => {
    if (!user) throw new Error("User not authenticated");
    if (pending.current) throw new Error("Deletion already in progress");
    pending.current = true;
    setLoading(true);
    try {
      const token = await user.getIdToken();
      await ChatAPI.deleteThread(threadId, token);
    } finally {
      pending.current = false;
      setLoading(false);
    }
  }, [user]);

  return { deleteThread, loading };
}
