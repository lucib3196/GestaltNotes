import type { ContentBlock } from "langchain";
import type { ReactNode } from "react";
import type { ImagePayload } from "../types/content";
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
function isImagePayload(value: unknown): value is ImagePayload {
  return (
    isRecord(value) &&
    value.type === "image_url" &&
    isRecord(value.image_url) &&
    typeof value.image_url.url === "string"
  );
}

export function extractMessageContent(content: unknown): string | unknown[] {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) return content;
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
    return typeof lastMsg.text === "string" ? lastMsg.text : "";
  }

  return msgContent.map((item, index) => {
    if (typeof item === "string") return <div key={index}>{item}</div>;
    if (isContentBlock(item))
      return (
        <div key={index}>{typeof item.text === "string" ? item.text : ""}</div>
      );
    if (isImagePayload(item))
      return (
        <figure
          key={index}
          className="my-3 w-fit max-w-full overflow-hidden rounded-xl p-2 shadow-sm"
        >
          <img
            src={item.image_url.url}
            alt={`Chat attachment ${index + 1}`}
            loading="lazy"
            decoding="async"
            className="block h-auto max-h-96 max-w-full rounded-lg object-contain"
          />
        </figure>
      );
  });
}
