import type { ReactNode } from "react";
import type { ContentBlock, BaseMessage, ToolMessage } from "langchain";
import type { CleanableContent } from "./instance/types";

type ImageUrl = {
  url: string;
};

type TextPayload = {
  type: "text";
  text: string;
};

type ImagePayload = {
  type: "image_url";
  image_url: ImageUrl;
};

type MessagePayload = TextPayload | ImagePayload;
type ChildChunk = ContentBlock | MessagePayload | string;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function isTextPayload(value: unknown): value is TextPayload {
  return isRecord(value) && value.type === "text" && typeof value.text === "string";
}

function isImagePayload(value: unknown): value is ImagePayload {
  return (
    isRecord(value) &&
    value.type === "image_url" &&
    isRecord(value.image_url) &&
    typeof value.image_url.url === "string"
  );
}

function isMessagePayload(value: unknown): value is MessagePayload {
  return isTextPayload(value) || isImagePayload(value);
}

function isMessagePayloadArray(value: unknown): value is MessagePayload[] {
  return Array.isArray(value) && value.every(isMessagePayload);
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

function isChildChunkArray(value: unknown): value is ChildChunk[] {
  return (
    Array.isArray(value) &&
    value.every(
      (item) =>
        typeof item === "string" ||
        isContentBlock(item) ||
        isMessagePayload(item),
    )
  );
}

function renderMessagePayload(item: MessagePayload, key: number): ReactNode {
  if (item.type === "text") {
    return <div key={key}>{item.text}</div>;
  }

  return (
    <img
      key={key}
      src={item.image_url.url}
      alt="message"
      className="max-w-2/5 rounded-md"
    />
  );
}

function chunkToText(item: ChildChunk): string {
  if (typeof item === "string") return item;
  if ("type" in item && item.type === "text" && typeof item.text === "string") {
    return item.text;
  }
  if ("type" in item && item.type === "image_generation_call") {
    return "image generated";
  }
  return "";
}

export function formatArgs(args: unknown): string {
  try {
    return JSON.stringify(args, null, 2);
  } catch {
    return String(args ?? "");
  }
}

export function normalizeContent(content: unknown): CleanableContent {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) return content as ContentBlock[];
  return String(content ?? "");
}

export function cleanChildren(
  content: ContentBlock[] | string | MessagePayload[] | ChildChunk[],
): string | ReactNode[] {
  if (typeof content === "string") {
    return content;
  }

  if (isContentBlockArray(content)) {
    if (!content.length) return "";

    const last = content.at(-1);
    if (!last) return "";

    if (last.type === "image_generation_call") {
      return "image generated";
    }

    return typeof last.text === "string" ? last.text : "";
  }

  if (isMessagePayloadArray(content)) {
    return content.map((item, index) => renderMessagePayload(item, index));
  }

  if (isChildChunkArray(content)) {
    const hasImage = content.some(
      (item) =>
        typeof item !== "string" &&
        "type" in item &&
        item.type === "image_url",
    );

    if (!hasImage) {
      return content.map(chunkToText).join("");
    }

    return content.map((item, index) => {
      if (typeof item === "string") return <div key={index}>{item}</div>;
      if (isMessagePayload(item)) return renderMessagePayload(item, index);
      if ("type" in item && item.type === "text" && typeof item.text === "string") {
        return <div key={index}>{item.text}</div>;
      }
      return null;
    });
  }

  return "";
}

export async function blobURLtoBase64(blobUrl: string): Promise<string> {
  const response = await fetch(blobUrl);
  const blob = await response.blob();
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.readAsDataURL(blob);
    reader.onloadend = () => resolve(reader.result as string);
    reader.onerror = reject;
  });
}





export function extractToolPayload(msg: ToolMessage): unknown {
  const c = msg.content;
  const cleaned = normalizeContent(c);
  let text: string | null = null;

  try {
    if (Array.isArray(cleaned)) {
      text = cleaned
        .map((b: any) => (typeof b?.text === "string" ? b.text : ""))
        .join("")
        .trim();
    } else if (typeof cleaned === "string") {
      text = cleaned;
    }

    if (!text) return c;
    return JSON.parse(text);
  } catch {
    return c;
  }
}
