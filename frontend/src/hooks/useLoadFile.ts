import { getDownloadURL, getStorage, ref } from "firebase/storage";
import { useCallback, useEffect, useState } from "react";

export type ResourceFile = { id: string; path: string; url: string };
type LoadResult = {
  key: string;
  files: ResourceFile[];
  errorsByPath: Record<string, string>;
};

export function useLoadFile(filePaths: readonly string[]) {
  const pathsKey = JSON.stringify([...new Set(filePaths.filter(Boolean))]);
  const [result, setResult] = useState<LoadResult | null>(null);
  const [attempt, setAttempt] = useState(0);
  const requestKey = `${attempt}:${pathsKey}`;
  const retry = useCallback(() => setAttempt((value) => value + 1), []);

  useEffect(() => {
    let active = true;
    const paths: string[] = JSON.parse(pathsKey);
    async function loadFiles() {
      const settled = await Promise.allSettled(paths.map(async (path) => ({
        id: path,
        path,
        url: await getDownloadURL(ref(getStorage(), path)),
      })));
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
    return () => { active = false; };
  }, [pathsKey, requestKey]);

  const current = result?.key === requestKey ? result : null;
  const errorsByPath = current?.errorsByPath ?? {};
  const failedCount = Object.keys(errorsByPath).length;
  return {
    files: current?.files ?? [],
    loading: filePaths.length > 0 && current === null,
    error: failedCount ? `${failedCount} source ${failedCount === 1 ? "PDF could" : "PDFs could"} not be loaded.` : null,
    errorsByPath,
    retry,
  };
}
