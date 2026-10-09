import type { Message } from "@langchain/langgraph-sdk";
import { renderContent } from "../../utils/messageParsing";
import type { MessageType } from "@langchain/core/messages";
import { RenderToolCall } from "../../../ToolCalls/RenderToolCalls";

import Markdown from "../../components/MardownRender";
const ChatBubbleBase =
  "my-2 max-w-full rounded-xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap shadow-soft";

const ChatBubbleStyles: Record<MessageType, string> = {
  ai: `${ChatBubbleBase} self-start border border-border bg-surface text-text`,
  human: `${ChatBubbleBase} self-end border border-border-strong bg-surface-strong text-text`,
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
