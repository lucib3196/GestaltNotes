import type { ToolMessage } from "langchain";
import type { Thread } from "../../../services";
import type { ThreadCreate } from "../../../services";
import type { ToolName } from "../tools";
import type { ThreadUpdate } from "../../../services/chat/types";

// Workspace item
export type WorkspaceItem = {
  id: string;
  tool: ToolName;
  rawMsg: ToolMessage;
};

type AssistantID = "agent_me116";

// Context types

export type ThreadState = {
  threadId: string | null;
  thread: Thread | null;
  threads: Thread[];
};

export type ThreadActions = {
  setThreadId: (threadId: string | null) => void;

  setThread: (thread: Thread | null) => void;

  setThreads: (threads: Thread[]) => void;

  updateThread: (update: Thread) => void;

  clearThread: () => void;
};
export type ThreadStore = ThreadState & ThreadActions;

export type WorkspaceState = {
  workspaceItems: WorkspaceItem[];
};
export type WorkspaceActions = {
  addWorkspaceItem: (item: WorkspaceItem) => void;
  clearWorkspace: () => void;
  appendToolMessage: (msg: ToolMessage) => void;
};

export type WorkspaceStore = WorkspaceState & WorkspaceActions;

export type AssistantState = {
  assistantId: AssistantID;
};

export type AssistantActions = {
  setAssistant: (assistant: AssistantID) => void;
};

export type AssistantStore = AssistantState & AssistantActions;

export type ChatState = {
  assistantId: AssistantID;
  theadId: string | null;
  thread: Thread | null;
  workspaceItems: WorkspaceItem[];
  sessionKey: number;
  loading: boolean;
  error: string | null;
};
export type ChatActions = {
  // Assistant Management
  setAssistant: (val: AssistantID) => void;

  // General refresh
  setSessionKey: () => void;
  // Thread management
  setThreadId: (threadId: string | null) => void;
  setThread: (
    threadId: string,
    token: string | null | undefined,
  ) => Promise<void>;
  selectThread: (threadId: string | null, token: string | null) => void;
  createdThread: (token: string, data: ThreadCreate) => Promise<Thread>;
  updateThread: (threadId: string, update: ThreadUpdate) => Promise<void>;
  getUserThreads: (token: string) => Promise<Thread[]>;
  onThreadId: (val: string, token: string) => Promise<void>;
  // Tool management
  setWorkspaceItems: (item: WorkspaceItem) => void;
  appendToolMessage: (msg: ToolMessage) => void;
};

export type ChatStore = ChatState & ChatActions;
