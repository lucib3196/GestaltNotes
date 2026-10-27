import type { Message } from "@langchain/langgraph-sdk";
import Markdown from "../../components/Markdown/MarkdownRenderer";
import { renderContent } from "../Chat/ui/messages/renderMessageContent";

import { getArtifactData } from "./artifacts";
import { resolveToolComponent } from "./resolveToolComponent";
export function RenderToolCall({ message }: { message: Message }) {
  if (message.type !== "tool") return null;

  const artifact: unknown = message.artifact;
  const data = getArtifactData(artifact);
  const entry = resolveToolComponent(message);
  const toolCompact = entry?.compact;
  const toolRender = entry && entry.render(data);

  if (message.status === "error") {
    return <div>Error</div>;
  }

  return (
    <div className={`flex min-w-0 flex-col`}>
      {message.content.length > 0 && (
        <div
          className={`self-start rounded-xl border border-border bg-surface text-sm text-text ${entry?.compact ? "px-3 py-2" : "px-4 py-3"}`}
        >
          <Markdown>{renderContent(message.content)}</Markdown>
          {toolCompact ? toolRender : null}
        </div>
      )}
      {!toolCompact ? toolRender : null}
    </div>
  );
}
