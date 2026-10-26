import type {
  Assistant,
  Attachment,
  PendingPrompt,
  RequestStatus,
} from "./types";
import type { Thread } from "../../services";
import type { ConfigSchema } from "./config";

export type ChatState = {
  config: ConfigSchema;
  assistant: Assistant;
  draftText: string;
  attachments: Attachment[];
  pendingPrompt: PendingPrompt | null;
};

export type ChatActions = {
  setModel: (model: ConfigSchema["model"]) => void;
  setAssistant: (id: Assistant) => void;
  setDraftText: (text: string) => void;
  addAttachments: (files: File[]) => void;
  removeAttachment: (id: string) => void;
  queuePrompt: (text: string) => void;
  clearPendingPrompt: (id: string) => void;
  clearDraft: () => void;
  startNewChat: ()=>void;
  updateConfig: (config: Partial<ConfigSchema>)=>void;
};

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

export type ThreadSlice = ThreadState & ThreadActions
export type ChatSlice = ChatActions & ChatState

export type ChatStore = ChatSlice & ThreadSlice
