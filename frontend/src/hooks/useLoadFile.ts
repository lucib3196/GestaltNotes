import { useCallback, useEffect, useState } from "react";
import { StorageAPI } from "../services/storage";
import { useAuth } from "../features/Auth";
export type ResourceFile = { id: string; path: string; url: string };
// Blob URLs returned by this callback are owned and cleaned up by the hook.
export type LoadFileUrl = (path: string) => Promise<string>;

type LoadResult = {
  key: string;
  files: ResourceFile[];
  errorsByPath: Record<string, string>;
};

export function useLoadFile(
  filePaths: readonly string[],
  loadFileUrl: LoadFileUrl,
) {
  const pathsKey = JSON.stringify([...new Set(filePaths.filter(Boolean))]);
  const [result, setResult] = useState<LoadResult | null>(null);
  const [attempt, setAttempt] = useState(0);
  const requestKey = `${attempt}:${pathsKey}`;
  const retry = useCallback(() => setAttempt((value) => value + 1), []);

  useEffect(() => {
    let active = true;
    const paths: string[] = JSON.parse(pathsKey);
    const blobUrls = new Set<string>();

    async function loadFiles() {
      const settled = await Promise.allSettled(
        paths.map(async (path) => {
          const url = await loadFileUrl(path);

          if (url.startsWith("blob:")) {
            if (active) {
              blobUrls.add(url);
            } else {
              URL.revokeObjectURL(url);
            }
          }

          return { id: path, path, url };
        }),
      );
      if (!active) return;
      const files: ResourceFile[] = [];
      const errorsByPath: Record<string, string> = {};
      settled.forEach((entry, index) => {
        if (entry.status === "fulfilled") files.push(entry.value);
        else errorsByPath[paths[index]] = "Could not load this PDF.";
      });
      setResult({ key: requestKey, files, errorsByPath });
    }
    void loadFiles();
    return () => {
      active = false;
      blobUrls.forEach((url) => URL.revokeObjectURL(url));
      blobUrls.clear();
    };
  }, [pathsKey, requestKey, loadFileUrl]);

  const current = result?.key === requestKey ? result : null;
  const errorsByPath = current?.errorsByPath ?? {};
  const failedCount = Object.keys(errorsByPath).length;
  return {
    files: current?.files ?? [],
    loading: filePaths.length > 0 && current === null,
    error: failedCount
      ? `${failedCount} source ${failedCount === 1 ? "PDF could" : "PDFs could"} not be loaded.`
      : null,
    errorsByPath,
    retry,
  };
}


export function useStorageFiles(storageKeys: readonly string[]) {
  const { user } = useAuth();

  const loadFileUrl = useCallback(
    async (storageKey: string) => {
      if (!user) {
        throw new Error("You must be signed in to load files.");
      }

      const token = await user.getIdToken();
      const blob = await StorageAPI.getFileByStorageKey(token, storageKey);
      return URL.createObjectURL(blob);
    },
    [user],
  );

  return useLoadFile(storageKeys, loadFileUrl);
}