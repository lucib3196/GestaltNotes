import { useCallback, useEffect, useRef, useState } from "react";
import { useAuth } from "../../Auth";
import { announcementError } from "./useAnnouncementRequest";

type Loader<T> = (token: string, signal: AbortSignal) => Promise<T>;

export function useAnnouncementQuery<T>(loader: Loader<T>, enabled = true) {
  const { user } = useAuth();
  const [state, setState] = useState<{
    uid: string;
    loader: Loader<T>;
    data: T | null;
    error: Error | null;
    loading: boolean;
  } | null>(null);
  const controller = useRef<AbortController | null>(null);

  const refetch = useCallback(async () => {
    controller.current?.abort();
    if (!user || !enabled) return null;
    const request = new AbortController();
    controller.current = request;
    setState((previous) => ({
      uid: user.uid,
      loader,
      data:
        previous?.uid === user.uid && previous.loader === loader
          ? previous.data
          : null,
      error: null,
      loading: true,
    }));
    try {
      const token = await user.getIdToken();
      if (request.signal.aborted) return null;
      const data = await loader(token, request.signal);
      if (!request.signal.aborted)
        setState({ uid: user.uid, loader, data, error: null, loading: false });
      return data;
    } catch (cause) {
      if (request.signal.aborted) return null;
      setState((previous) => ({
        uid: user.uid,
        loader,
        data:
          previous?.uid === user.uid && previous.loader === loader
            ? previous.data
            : null,
        error: announcementError(cause),
        loading: false,
      }));
      return null;
    }
  }, [user, enabled, loader]);

  useEffect(() => {
    let active = true;
    queueMicrotask(() => {
      if (active) void refetch();
    });
    return () => {
      active = false;
      controller.current?.abort();
    };
  }, [refetch]);

  const current =
    enabled && user && state?.uid === user.uid && state.loader === loader
      ? state
      : null;
  return {
    data: current?.data ?? null,
    loading: Boolean(enabled && user && (!current || current.loading)),
    error: current?.error ?? null,
    refetch,
  };
}
