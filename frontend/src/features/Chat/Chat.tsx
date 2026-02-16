import { useStream } from "@langchain/langgraph-sdk/react";
import { ChatMessage, ChatContainer, ChatInput } from "../../components/Chat";
import { useState } from "react";

export default function Chat() {
  const [message, setMessage] = useState<string>("");
  const stream = useStream({
    assistantId: "agent_me135",
    // Local development
    apiUrl: import.meta.env.VITE_PRODUCTION_URL,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
  });

  const handleSubmit = (message: string) => {
    stream.submit({
      messages: [{ content: message, type: "human" }],
    });
  };

  return (
    <ChatContainer className="flex flex-col  h-min-[400px] border border-slate-200 rounded-xl bg-white shadow-sm">
      {/* Scrollable message area */}
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-2">
        {stream.messages.map((message, idx) => {
          return <ChatMessage key={idx} message={message} id={idx} />;
        })}

        {stream.isLoading && (
          <div className="text-sm text-slate-400">Typing...</div>
        )}
      </div>

      {/* Input area */}
      <div className="border-t border-slate-200 p-3 bg-slate-50">
        <ChatInput
          value={message}
          setValue={setMessage}
          onSubmit={() => { handleSubmit(message); setMessage("") }}
        />
      </div>
    </ChatContainer>
  );
}
