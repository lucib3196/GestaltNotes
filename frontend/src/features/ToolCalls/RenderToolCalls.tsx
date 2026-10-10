import type { Message } from "@langchain/langgraph-sdk";
import Markdown from "../../components/Markdown/MarkdownRenderer";
import { renderContent } from "../Chat/ui/messages/renderMessageContent";

import { getArtifactData } from "./artifacts";
import { resolveToolComponent } from "./resolveToolComponent";
export function RenderToolCall({ message }: { message: Message }) {
  if (message.type !== "tool") return null;

  const artifact: unknown = message.artifact;
  const data = getArtifactData(artifact);
  const renderer = resolveToolComponent(message);
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
