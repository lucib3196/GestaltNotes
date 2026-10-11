import type { Message } from "@langchain/langgraph-sdk";
import MessageBubble from "./MessageBubble";

export default function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div
      className="flex min-w-0 flex-col gap-4"
      role="log"
      aria-label="Conversation"
      id="message-list"
    >
      {messages.map((message, index) => {
        return <MessageBubble key={message.id ?? index} message={message} />;
      })}
    </div>
  );
}
