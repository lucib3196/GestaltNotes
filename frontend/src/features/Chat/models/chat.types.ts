import {
  AIMessage,
  HumanMessage,
  ToolMessageChunk,
  ContentBlock,
} from "@langchain/core/messages";

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

export type ImageUrl = {
  url: string;
};

export type TextPayload = {
  type: "text";
  text: string;
};

export type ImagePayload = {
  type: "image_url";
  image_url: ImageUrl;
};

export type MessagePayload = TextPayload | ImagePayload;
export type ChildChunk = ContentBlock | MessagePayload | string;
