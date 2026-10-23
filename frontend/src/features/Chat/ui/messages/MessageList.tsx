import type { Message } from "@langchain/langgraph-sdk";
import MessageBubble from "./MessageBubble";

export default function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div
      className="mx-auto flex w-full max-w-4xl min-w-0 flex-col gap-6 sm:gap-8"
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
