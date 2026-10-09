import {
  AIMessage,
  HumanMessage,
  ToolMessageChunk,
  ContentBlock,
} from "@langchain/core/messages";

export type TextPayload = {
  type: "text";
  text: string;
};

export type ImagePayload = {
  type: "image_url";
  image_url: string;
};
export type MessagePayload = TextPayload | ImagePayload;

export type RendableContent = ContentBlock[] | string;
