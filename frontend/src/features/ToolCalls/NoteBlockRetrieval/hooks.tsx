import { useMemo } from "react";
import type { NoteBlockDocuments } from "./schema";

export function useSources(documents: NoteBlockDocuments) {
  return useMemo(() => {
    const sources = new Map<string, { path: string; title: string }>();

    for (const { metadata } of documents) {
      const path = metadata.storage_key?.trim();
      if (!path) continue;

      sources.set(path, {
        path,
        title: metadata.filename || metadata.title,
      });

      return [...sources.values()];
    }
  }, [documents]);
}
