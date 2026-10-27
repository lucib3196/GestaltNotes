import { useEffect, useState } from "react";
import { useAuth } from "../Auth";
import { fetchNoteBlocks } from "./api";
import type { NoteBlock } from "./schemas";

type RequestState = {
  courseId: string;
  fileId: string;
  userId: string;
  blocks: NoteBlock[];
  error: string | null;
};

export function useNoteBlocks(courseId: string, fileId: string) {
  const { user, loading: authLoading } = useAuth();
  const [result, setResult] = useState<RequestState | null>(null);

  useEffect(() => {
    if (authLoading || !user || !courseId || !fileId) return;
    const controller = new AbortController();

    async function load() {
      try {
        const token = await user!.getIdToken();
        if (controller.signal.aborted) return;
        const blocks = await fetchNoteBlocks(
          token,
          courseId,
          fileId,
          controller.signal,
        );
        if (!controller.signal.aborted) {
          setResult({
            courseId,
            fileId,
            userId: user!.uid,
            blocks,
            error: null,
          });
        }
      } catch {
        if (!controller.signal.aborted) {
          setResult({
            courseId,
            fileId,
            userId: user!.uid,
            blocks: [],
            error: "Unable to load note blocks. Please try again.",
          });
        }
      }
    }

    void load();
    return () => controller.abort();
  }, [authLoading, user, courseId, fileId]);

  const current =
    result?.courseId === courseId &&
    result?.fileId === fileId &&
    result?.userId === user?.uid
      ? result
      : null;
  const missingSelection = !courseId || !fileId;
  const error = authLoading
    ? null
    : !user
      ? "Sign in to view note blocks."
      : missingSelection
        ? "Select a course and file to view note blocks."
        : (current?.error ?? null);

  return {
    blocks:
      !authLoading && user && !missingSelection ? (current?.blocks ?? []) : [],
    loading: authLoading || (!!user && !missingSelection && !current),
    error,
  };
}
