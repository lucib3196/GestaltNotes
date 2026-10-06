import type { Thread } from "../../services";
export function threadsById(threads: Thread[]): Record<string, Thread> {
  const byId: Record<string, Thread> = {};
  for (const t of threads) {
    if (!t.id) continue;
    byId[t.id] = t;
  }
  return byId;
}
