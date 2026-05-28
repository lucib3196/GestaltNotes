import { BaseMessage, ToolMessage } from "langchain";
import { TOOL_NAMES, type ToolName } from "./types";

export function isToolMessage(msg: BaseMessage): msg is ToolMessage {
  return (
    msg.type === "tool" &&
    typeof (msg as { tool_call_id?: unknown }).tool_call_id === "string"
  );
}

export function getSupportedToolMessage(
  msg: BaseMessage,
): { name: ToolName; msg: ToolMessage } | null {
  if (!isToolMessage(msg)) return null;

  const toolName = msg.name ?? undefined;
  if (!toolName) {
    return null;
  }
  const isValid = (TOOL_NAMES as readonly string[]).includes(toolName);
  if (!isValid) return null;

  return {
    name: toolName as ToolName,
    msg,
  };
}
