import { useStream } from "@langchain/langgraph-sdk/react";
import {
  ChatMessage,
  ChatContainer,
  ChatInput,
  SourceSection,
} from "../../components/Chat";
import { useEffect, useState } from "react";
import { type ValidAgent } from "./context";
import { UseLectureChatContext, type LectureArtifact } from "./context";
import { type Message } from "@langchain/langgraph-sdk";
import { DropDown } from "../../components/DropDown";

export default function Chat() {
  const [message, setMessage] = useState<string>("");

  const { sources, setSources, agent, setAgent, threadId, setThreadId } =
    UseLectureChatContext();

  useEffect(() => {
    setThreadId(crypto.randomUUID());
  }, [agent]);

  const stream = useStream({
    assistantId: agent,
    apiUrl: import.meta.env.VITE_LOCAL_URL,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    onThreadId: setThreadId,
  });

  const handleArtifacts = (message: Message) => {
    if (message.type !== "tool" || !message.artifact) return;

    const artifacts = (
      Array.isArray(message.artifact)
        ? message.artifact
        : Object.values(message.artifact)
    ) as LectureArtifact[];

    setSources(artifacts);
  };

  const handleSubmit = () => {
    if (!message.trim()) return;

    stream.submit({
      messages: [{ content: message, type: "human" }],
    });

    setMessage("");
  };

  return (
    <div className="flex flex-col max-w-3xl mx-auto h-[80vh]">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-semibold text-slate-800">
          Lecture Tutor: Thread {threadId}
        </h2>

        <DropDown
          options={["agent_me135", "agent_me118"]}
          selected={agent}
          label="Select Course"
          setSelected={(v) => setAgent(v as ValidAgent)}
        />
      </div>

      {/* Chat Container */}
      <ChatContainer className="flex flex-col flex-1 border border-slate-200 rounded-2xl bg-white shadow-sm overflow-hidden">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-5 space-y-3 bg-slate-50">
          {stream.messages.map((msg, idx) => {
            handleArtifacts(msg);
            return <ChatMessage key={idx} message={msg} id={idx} />;
          })}

          {stream.isLoading && (
            <div className="text-sm text-slate-400 animate-pulse">
              Assistant is thinking...
            </div>
          )}

          {sources.length > 0 && (
            <div className="pt-2">
              <SourceSection sources={sources} />
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-slate-200 bg-white px-5 py-4">
          <ChatInput
            value={message}
            setValue={setMessage}
            onSubmit={handleSubmit}
          />
        </div>
      </ChatContainer>
    </div>
  );
}
