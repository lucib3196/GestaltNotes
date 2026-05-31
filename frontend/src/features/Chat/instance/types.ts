import type { ContentBlock, ToolMessage } from "langchain";
import type { Thread } from "../../../services";
import {
  AIMessage,
  HumanMessage,
  ToolMessageChunk,
} from "@langchain/core/messages";
import type { ThreadCreate } from "../../../services";
import type { ToolName } from "../tools";
import type { ThreadUpdate } from "../../../services/chat/types";

export type ToolType = "invokation" | "tool_result";
export type MessageType = "ai" | "human" | "tool";

export type ChatBubbleRender =
  | { bubble: "human"; msg: HumanMessage }
  | { bubble: "ai"; msg: AIMessage; showTools?: boolean }
  | { bubble: "tool"; msg: ToolMessageChunk };

export interface AIMessageBubbleProps {
  type?: "ai";
  msg: AIMessage;
  showTools?: boolean;
}
export interface HumanBubbleProps {
  type?: "human";
  msg: HumanMessage;
}
export interface ToolBubbleProps {
  type?: "tool";
  msg: ToolMessageChunk;
}

export type CleanableContent = ContentBlock[] | string;

export type UnknownRecord = Record<string, unknown>;

export type ConversationStarter = {
  id: string;
  label: string;
  message: string;
  description?: string;
  disabled?: boolean;
};

export interface ConversationStartersProps {
  starters: ConversationStarter[];
  disabled?: boolean;
  onSelectStarter: (starter: ConversationStarter) => void;
}

// Workspace item
export type WorkspaceItem = {
  id: string;
  tool: ToolName;
  rawMsg: ToolMessage;
};

type AssistantID = "agent_me116";

// Context types
export type ChatState = {
  assistantId: AssistantID;
  theadId: string | null;
  thread: Thread | null;
  workspaceItems: WorkspaceItem[];
  sessionKey: number;
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
