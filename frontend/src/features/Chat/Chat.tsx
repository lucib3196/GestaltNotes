import { useStream } from "@langchain/langgraph-sdk/react";
import {
  ChatMessage,
  ChatContainer,
  ChatInput,
  ChatSideBar,
  SourceSection,
  type ChatThread,
} from "../../components/Chat";
import { useRef, useState, useEffect } from "react";
import { type ValidAgent } from "./context";
import { UseLectureChatContext, type LectureArtifact } from "./context";
import { type Message } from "@langchain/langgraph-sdk";
import { DropDown } from "../../components/DropDown";

let threadCreated = false;

export default function Chat() {
  const [message, setMessage] = useState<string>("");
  const [chats, setChats] = useState<ChatThread[]>([]);

  const { sources, setSources, agent, setAgent, threadId, setThreadId } =
    UseLectureChatContext();

const pendingMessage = useRef<string | null>(null);

const stream = useStream({
  assistantId: agent,
  apiUrl: import.meta.env.VITE_PRODUCTION_URL,
  apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
  threadId: threadId ?? undefined,
  onThreadId: async (id: string) => {
    // deals with the strict mode
    if (threadCreated) return;
      threadCreated = true;
    setThreadId(id);
    

    // First message — create the FastAPI thread with LangGraph's ID
    const response = await fetch(`${import.meta.env.VITE_LOCAL_URL}threads`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        thread_id: id,
        user_id: "00000000-0000-0000-0000-000000000001",
        course_id: "86d28f0c-1a7d-4346-8922-0f95cbfffcdd",
        title: pendingMessage.current ?? "New Chat",
        agent: agent,
      }),
    });
    const data = await response.json();
    setChats((prev) => [{ id, title: data.title ?? "New Chat" }, ...prev]);

    // Now save the pending human message
    if (pendingMessage.current) {
      await fetch(`${import.meta.env.VITE_LOCAL_URL}threads/${id}/messages`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: "human",
          content: pendingMessage.current,
        }),
      });
      pendingMessage.current = null;
    }
  },
});

const loadThread = async (id: string) => {
  threadCreated = true;
  setThreadId(id);
};

const handleSubmit = async () => {
  if (!message.trim()) return;

  if (!threadId) {
    // First message — store it and let onThreadId handle saving it
    pendingMessage.current = message;
  } else {
    // Subsequent messages — thread already exists, save directly
    await fetch(`${import.meta.env.VITE_LOCAL_URL}threads/${threadId}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        role: "human",
        content: message,
      }),
    });
  }

  stream.submit({
    messages: [{ content: message, type: "human" }],
  });

  setMessage("");
};

  const handleArtifacts = (message: Message) => {
    if (message.type !== "tool" || !message.artifact) return;

    const artifacts = (
      Array.isArray(message.artifact)
        ? message.artifact
        : Object.values(message.artifact)
    ) as LectureArtifact[];

    setSources(artifacts);
  };

  useEffect(() => {
  if (!stream.isLoading && stream.messages.length > 0 && threadId) {
    const lastMessage = stream.messages[stream.messages.length - 1];
    if (lastMessage.type === "ai") {
      fetch(`${import.meta.env.VITE_LOCAL_URL}threads/${threadId}/messages`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: "ai",
          content: String(lastMessage.content),
        }),
      });
    }
  }
}, [stream.isLoading]);

  return (
    <div className="flex flex-col max-w-6xl mx-auto h-[80vh]">
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
      <div className="flex flex-1 min-h-0 items-stretch">
        <ChatSideBar chats={chats}
          activeChatId={threadId ?? undefined}
          onSelectChat={(id) => loadThread(id)}
          onNewChat={() => {
            threadCreated = false;
            setThreadId(null);
            stream.stop?.();
          }} />
          <div className="flex-1 min-w-0">
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
      </div>
    </div>
  );
}
