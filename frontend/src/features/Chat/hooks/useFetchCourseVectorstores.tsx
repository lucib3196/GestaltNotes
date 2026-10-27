import {
  EnrollmentsAPI,
  type EnrollmentChatContext,
} from "../../../services/enrollments";
import { useAuth } from "../../Auth";
import { useState, useEffect } from "react";

export function useFetchCourseVectorstore() {
  const { user } = useAuth();
  const [configs, setConfigs] = useState<EnrollmentChatContext[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let active = true;

    async function fetchCourseVectorStores() {
      if (!active) return;
      setConfigs([]);
      setError(null);
      setLoading(Boolean(user));
      if (!user) return;

      try {
        const token = await user.getIdToken();
        if (!active) return;
        const configs = await EnrollmentsAPI.getChatContext(token);
        if (active) setConfigs(configs);
      } catch (err) {
        if (active) {
          setError(
            err instanceof Error ? err : new Error("Failed to fetch courses."),
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    void fetchCourseVectorStores();
    return () => {
      active = false;
    };
  }, [user]);
  return { configs, loading, error };
}
