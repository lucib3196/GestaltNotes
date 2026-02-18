import { useStream } from "@langchain/langgraph-sdk/react";
import { ChatMessage, ChatContainer, ChatInput, SourceSection } from "../../components/Chat";
import { useState } from "react";
import { UseLectureChatContext, type LectureArtifact } from "./context";
import { type Message } from "@langchain/langgraph-sdk";


export default function Chat() {
  const [message, setMessage] = useState<string>("");
  const { sources, setSources, agent } = UseLectureChatContext()

  const stream = useStream({
    assistantId: agent,
    // Local development
    apiUrl: import.meta.env.VITE_LOCAL_URL,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
  });


  const handleArtifacts = (message: Message) => {
    if (message.type === "tool") {
      if (!message.artifact) {
        return
      }
      const artifacts = (Array.isArray(message.artifact) ? message.artifact : Object.values(message.artifact)) as LectureArtifact[]
      setSources(artifacts)
    }
  }

  const handleSubmit = (message: string) => {
    stream.submit({
      messages: [{ content: message, type: "human" }],
    });
  };

  console.log("Current sources", sources)


  return (<>
    <ChatContainer className="flex flex-col  h-min-[400px] border border-slate-200 rounded-xl bg-white shadow-sm">
      {/* Scrollable message area */}
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-2">
        {stream.messages.map((message, idx) => {
          // Gets the message and addes the sources
          handleArtifacts(message)
          return <ChatMessage key={idx} message={message} id={idx} />;
        })}

        {stream.isLoading && (
          <div className="text-sm text-slate-400">Typing...</div>
        )}

        {sources.length > 0 && <SourceSection sources={sources} />}

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
  </>
  );
}
