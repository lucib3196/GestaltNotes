import { useAuth } from "../../../context";
import { UseLectureChatContext } from "../../../context/ChatContext";
import { type ThreadCreate } from "../components/Chat";
import { api } from "../../../config";

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

export const useUserThreads = () => {
  const { user } = useAuth();

  const getThreads = async (): Promise<Thread[]> => {
    try {
      const token = await user?.getIdToken();
      const response = await api.get<Thread[]>("/users/thread/", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.data) {
        throw new Error("Failed to generate thread id");
      }

      return response.data;
    } catch (error) {
      console.error("Error generating thread:", error);
      throw error;
    }
  };
  return { getThreads };
};
