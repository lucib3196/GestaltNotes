import type { Thread } from "../../../services";
import type { ThreadCreate } from "../../../services";

import type { ThreadUpdate } from "../../../services/chat/types";

// Workspace item

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

export type AssistantState = {
  assistantId: AssistantID;
};

export type AssistantActions = {
  setAssistant: (assistant: AssistantID) => void;
};

export type AssistantStore = AssistantState & AssistantActions;

export type ChatState = {
  assistantId: AssistantID;
};
export type ChatActions = {
  // Assistant Management
  setAssistant: (val: AssistantID) => void;
};

export type ChatStore = ChatState & ChatActions;
