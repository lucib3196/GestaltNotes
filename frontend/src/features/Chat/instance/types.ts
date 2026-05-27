import type { ContentBlock } from "langchain";
import type { Thread } from "../../../services";
import {
  AIMessage,
  HumanMessage,
  ToolMessageChunk,
} from "@langchain/core/messages";
import type { ThreadCreate } from "../../../services";


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


// Context types
export type ChatState = {
  theadId: string | null;
};
export type ChatActions = {
  setThreadId: (threadId: string | null) => void;
  createdThread: (token: string, data: ThreadCreate) => Promise<Thread>;
  getUserThreads: (token: string) => Promise<Thread[]>;
  onThreadId: (val: string) => void;
};

export type ChatStore = ChatState & ChatActions;


