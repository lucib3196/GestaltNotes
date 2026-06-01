import { BaseMessage, ToolMessage } from "langchain";
import { TOOL_NAMES, type ToolName } from "./models/tools.types";
import { normalizeContent } from "../Chat/utils";
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

export function extractToolPayload(msg: ToolMessage): unknown {
  // First try with the artifact
  const artifact = msg.artifact;
  if (artifact) {
    if (typeof artifact === "object") return artifact;
    else if (typeof artifact === "string") return JSON.parse(artifact);
    else return artifact;
  }
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
