import type { Message } from "@langchain/langgraph-sdk";
import { getArtifactKind } from "./artifacts";
import { toolCallRegistry } from "./registry";

export function resolveToolComponent(message: Message) {
  if (message.type !== "tool") return null;
  const kind = getArtifactKind(message.artifact);
  if (kind && Object.hasOwn(toolCallRegistry, kind))
    return toolCallRegistry[kind];
  if (message.name && Object.hasOwn(toolCallRegistry, message.name))
    return toolCallRegistry[message.name];
  return null;
}
