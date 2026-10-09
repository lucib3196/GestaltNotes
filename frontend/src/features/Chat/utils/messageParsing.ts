import type { ContentBlock } from "langchain";
import type { RendableContent } from "../types";
import type { ReactNode } from "react";
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
function isContentBlock(value: unknown): value is ContentBlock {
  return (
    isRecord(value) &&
    "type" in value &&
    "text" in value &&
    typeof value.text === "string"
  );
}
function isContentBlockArray(value: unknown): value is ContentBlock[] {
  return Array.isArray(value) && value.every(isContentBlock);
}

export function extractMessageContent(content: unknown): RendableContent {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) return content as ContentBlock[];
  return String(content ?? "");
}

export function renderContent(content: unknown): string | ReactNode[] {
  const msgContent = extractMessageContent(content);
  if (typeof msgContent === "string") {
    return msgContent;
  }
  if (isContentBlockArray(msgContent) && msgContent.length) {
    const lastMsg = msgContent.at(-1);
    if (!lastMsg) return "";
    if (lastMsg.type === "image_generation_call") {
      return "image generated";
    }
    console.log("Got content block")
    return typeof lastMsg.text === "string" ? lastMsg.text : "";
  }
  return "";
}
