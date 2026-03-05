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
import { useGenerateThread, useUserThreads } from "../hooks/hooks";
import { useAuth } from "../../../context";

export type ThreadCreate = {
  thread_id: string | null;
  user_id: string | null;
  course_id: string | null;
  title: string | null;
  agent: string | null;
};

export default function Chat() {
  const [message, setMessage] = useState<string>("");
  const [chats, setChats] = useState<ChatThread[]>([]);
  const [created, setCreated] = useState<boolean>(false);
  const { getThreads } = useUserThreads();
  const { user } = useAuth();

  // Context
  const { sources, setSources, agent, setAgent, threadId, setThreadId } =
    UseLectureChatContext();
  const pendingMessage = useRef<string | null>(null);
  const generateThread = useGenerateThread();
  // Fetch all the users previos convos
  useEffect(() => {
    const fetch = async () => {
      const oldThreads = await getThreads();
      setChats(
        oldThreads.map((t) => ({ title: t.title, id: t.id }) as ChatThread),
      );
    };
    fetch();
  }, [user]);

  const handleNewChats = async () => {
    stream.stop?.();
    setThreadId(null);
    setCreated(false);
  };

  const stream = useStream({
    assistantId: agent,
    apiUrl: import.meta.env.VITE_PRODUCTION_URL,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    threadId: threadId ?? undefined,

    onThreadId: async (id: string) => {
      if (created) return;
      setCreated(true);

      const threadData: ThreadCreate = {
        agent,
        thread_id: id,
        course_id: null,
        user_id: null,
        title: pendingMessage.current ?? "New Chat",
      };
      const response = await generateThread(threadData);
      setThreadId(id);
      setChats((prev) => [
        { id, title: response.title ?? "New Chat" },
        ...prev,
      ]);
    },
  });

  const handleSubmit = async () => {
    try {
      if (!message.trim()) {
        return;
      }

      if (!threadId) {
        // First message so store it and let onThreadId handle saving it
        pendingMessage.current = message;
      } else {
        // thread already exists, save directly
        await api.post(`/threads/${threadId}/messages`, {
          role: "human",
          content: message,
        });
      }

      stream.submit({
        messages: [{ content: message, type: "human" }],
      });
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
          onSelectChat={(id) => {
            setThreadId(id);
          }}
          onNewChat={handleNewChats}
        />
        <div className="flex-1 min-w-0">
          {/* Chat Container */}
          <ChatContainer className="flex w-full h-full">
            {/* Messages */}
            <div className="flex-1 h-full overflow-y-auto px-6 py-5 space-y-3 bg-slate-50">
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

            <div className="w-full m-2 p-1">
              <ChatInput
                value={message}
                setValue={setMessage}
                onSubmit={() => {
                  handleSubmit();
                }}
              />
            </div>
          </ChatContainer>
        </div>
      </div>
    </div>
  );
}
