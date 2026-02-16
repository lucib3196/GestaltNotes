import { type MessageType } from "./config";
import { type ToolMessage } from "@langchain/langgraph-sdk";
export function isMessageType(value: string): value is MessageType {
  return value === "ai" || value === "human" || value === "tool";
}

export function normalizeType(type: string): MessageType {
  return isMessageType(type) ? type : "ai";
}

export function parseToolResult(result?: ToolMessage): {
  status: string;
  content: string;
} {
  if (!result) return { status: "pending", content: "" };

  console.log("Here is the result", result);

  try {
    return JSON.parse(result.content as string);
  } catch {
    return { status: "success", content: String(result.content) };
  }
}
