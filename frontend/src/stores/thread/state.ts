import type { Thread } from "../../services";



export type RequestStatus = "idle" | "loading" | "success" | "error";
export type ThreadState = {
  threadsById: Record<string, Thread>;
  threadIds: string[];
  activeThreadId: string | null;
  listStatus: RequestStatus;
  listError: string | null;
  activeThreadStatus: RequestStatus;
  activeThreadError: string | null;
};

export type ThreadActions = {
  selectThread: (id: string) => void;
  setThreads: (threads: Thread[]) => void;
  upsertThread: (thread: Thread) => void;
  removeThread: (id: string) => void;
  setListStatus: (status: RequestStatus, error?: string) => void;
  setActiveThreadStatus: (status: RequestStatus, error?: string) => void;
};

export type ThreadStore = ThreadActions & ThreadState;
