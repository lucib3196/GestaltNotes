import { useCallback, useRef, useState } from "react";
import axios from "axios";
import { useAuth } from "../../Auth";

export function announcementError(error: unknown): Error {
  if (axios.isAxiosError(error)) {
    const detail: unknown = error.response?.data?.detail;
    if (typeof detail === "string") return new Error(detail);
    if (error.response?.status === 401)
      return new Error("Your session has expired. Please sign in again.");
    if (error.response?.status === 403)
      return new Error("You do not have permission to manage announcements.");
    if (error.response?.status === 422)
      return new Error("Please check the announcement fields and try again.");
  }
  return error instanceof Error
    ? error
    : new Error("Could not complete the announcement request.");
}

export function useAnnouncementRequest() {
  const { user } = useAuth();
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const inFlight = useRef(false);

  const run = useCallback(
    async <T>(operation: (token: string) => Promise<T>): Promise<T> => {
      if (inFlight.current)
        throw new Error("An announcement request is already in progress.");
      inFlight.current = true;
      setPending(true);
      setError(null);
      try {
        if (!user) throw new Error("Sign in to continue.");
        return await operation(await user.getIdToken());
      } catch (cause) {
        const failure = announcementError(cause);
        setError(failure);
        throw failure;
      } finally {
        inFlight.current = false;
        setPending(false);
      }
    },
    [user],
  );

  return { run, pending, error };
}
