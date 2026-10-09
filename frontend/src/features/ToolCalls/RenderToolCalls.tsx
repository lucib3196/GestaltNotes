import type { Message } from "@langchain/langgraph-sdk";
import Markdown from "../../components/Markdown/MarkdownRenderer";
import { renderContent } from "../Chat/ui/messages/renderMessageContent";
import { toolCallRegistry } from "./registry";

export function RenderToolCall({ message }: { message: Message }) {
  if (message.type !== "tool") return null;

  const artifact: unknown = message.artifact;
  const data =
    typeof artifact === "object" && artifact !== null && "data" in artifact
      ? artifact.data
      : undefined;
  const renderer =
    message.name && Object.hasOwn(toolCallRegistry, message.name)
      ? toolCallRegistry[message.name]
      : undefined;

  return (
    <div className="flex min-w-0 flex-col gap-3">
      {message.content.length > 0 && (
        <div className="self-start rounded-xl border border-border bg-surface px-4 py-3 text-sm text-text">
          <Markdown>{renderContent(message.content)}</Markdown>
        </div>
      )}
      {renderer && renderer(data)}
    </div>
  );
}
