import { useStream } from "@langchain/langgraph-sdk/react";

import ChatMessage from "./ChatMessage";
import ChatContainer from "./ChatContainer";
import ChatSideBar from "./ChatSideBar";
import ChatInput from "./ChatInput";
import { type ChatThread } from "./ChatSideBar";
import { useRef, useState, useEffect } from "react";
import SourceSection from "./Sources";
import {
  UseLectureChatContext,
  type LectureArtifact,
  type ValidAgent,
} from "../../../context/ChatContext";
import { type Message } from "@langchain/langgraph-sdk";
import { DropDown } from "../../../components/DropDown";
import api from "../../../config/api";
import { useAuth } from "../../../context";

type ThreadCreate = {
  thread_id: string | null;
  user_id: string | null;
  course_id: string | null;
  title: string | null;
  agent: string | null;
};
let threadCreated = false;

export default function Chat() {
  const [message, setMessage] = useState<string>("");
  const [chats, setChats] = useState<ChatThread[]>([]);

  // Context
  const { sources, setSources, agent, setAgent, threadId, setThreadId } =
    UseLectureChatContext();
  const { user } = useAuth();

  const pendingMessage = useRef<string | null>(null);

  const stream = useStream({
    assistantId: agent,
    apiUrl: import.meta.env.VITE_PRODUCTION_URL,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    threadId: threadId ?? undefined,
    onThreadId: async (id: string) => {
      if (threadCreated) return;
      threadCreated = true;
      setThreadId(id);

      // Construct the payload for the post
      let threadData = {
        agent: agent,
        thread_id: id,
        course_id: null,
        user_id: null,
        title: pendingMessage.current ?? "New Chat",
      } as ThreadCreate;
      const token = await user?.getIdToken();
      // First message so create the FastAPI thread with LangGraph's Thread ID
      const response = await api.post("/users/thread/", threadData, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = response.data;
      setChats((prev) => [{ id, title: data.title ?? "New Chat" }, ...prev]);

      // Now save the pending human message
      if (pendingMessage.current) {
        await api.post(`/threads/${encodeURIComponent(id)}/messages`, {
          role: "human",
          content: pendingMessage.current,
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
    console.log("Handling submit", threadId);
    try {
      if (!message.trim()) {
        console.log("Current message is None", message);
        return;
      }

      if (!threadId) {
        // First message so store it and let onThreadId handle saving it
        pendingMessage.current = message;
      } else {
        console.log("Passed thread", threadId);
        // thread already exists, save directly
        let response = await api.post(`/threads/${threadId}/messages`, {
          role: "human",
          content: message,
        });
        console.log("Okay passed", response);
      }
      console.log("Hello message", message);

      stream.submit({
        messages: [{ content: message, type: "human" }],
      });
      console.log("Current message", message);
      setMessage("");
    } catch (error: any) {
      console.log("Error", error);
    }
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
        api.post(`/threads/${threadId}/messages`, {
          role: "ai",
          content: String(lastMessage.content),
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
        <ChatSideBar
          chats={chats}
          activeChatId={threadId ?? undefined}
          onSelectChat={(id) => loadThread(id)}
          onNewChat={() => {
            threadCreated = false;
            setThreadId(null);
            stream.stop?.();
          }}
        />
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
                onSubmit={() => {
                  handleSubmit();
                  console.log("Clicked", message);
                }}
              />
            </div>
          </ChatContainer>
        </div>
      </div>
    </div>
  );
}
