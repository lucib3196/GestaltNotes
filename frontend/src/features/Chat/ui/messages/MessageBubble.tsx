import type { Message } from "@langchain/langgraph-sdk";
import { renderContent } from "./renderMessageContent";
import type { MessageType } from "@langchain/core/messages";
import { RenderToolCall } from "../../../ToolCalls/RenderToolCalls";

import Markdown from "../../../../components/Markdown/MarkdownRenderer";
const ChatBubbleBase =
  "min-w-0 max-w-full rounded-lg px-4 py-3 text-sm leading-relaxed sm:max-w-[90%]";

const ChatBubbleStyles: Record<MessageType, string> = {
  ai: `${ChatBubbleBase} self-start border border-border bg-surface text-text`,
  human: `${ChatBubbleBase} self-end border border-accent/25 bg-accent/10 text-text sm:max-w-[80%]`,
  tool: `${ChatBubbleBase} self-start border border-accent/35 bg-surface-muted text-text`,
  system: `${ChatBubbleBase} self-start border border-border bg-surface text-text`,
};
export default function MessageBubble({ message }: { message: Message }) {
  if (message.type === "tool") return <RenderToolCall message={message} />;
  return (
    <div className={ChatBubbleStyles[message.type]}>
      <Markdown>{renderContent(message.content)}</Markdown>
    </div>
  );
}
