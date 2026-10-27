import { useMemo } from "react";
import type { NoteBlockDocuments } from "./schema";

type MappedSource = {
  path: string;
  title: string;
  extension?: string | null;
  count: number;
};
export function useSources(documents: NoteBlockDocuments) {
  return useMemo(() => {
    const sources = new Map<string, MappedSource>();

    console.log("Extracting sources", documents);

    for (const { metadata } of documents) {
      const path = metadata.storage_key?.trim();
      if (!path) continue;

      const existing = sources.get(path);
      if (existing) {
        existing.count += 1;
      } else {
        sources.set(path, {
          path,
          title: metadata.filename || metadata.title,
          extension: metadata.content_type,
          count: 1,
        });
      }
    }
    return [...sources.values()];
  }, [documents]);
}
