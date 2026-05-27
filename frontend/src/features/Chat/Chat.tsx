import { useStream } from "@langchain/langgraph-sdk/react";
import { MathJax } from "better-react-mathjax";
import { AIMessage, HumanMessage, ToolMessage } from "langchain";
import { useCallback, useEffect, useState } from "react";
import { GiHamburgerMenu } from "react-icons/gi";

import { streamURL } from "../../config/api";
import { useAuth } from "../../context";
import type { Thread, ThreadCreate } from "../../services";
import { ChatContainer, ChatInput } from "./components";
import { AIBubble, HumanBubble } from "./components/ChatMessage";
import { useChatContext } from "./instance";
import RenderToolCalls from "./tools/renderToolCalls";
import { blobURLtoBase64 } from "./utils";
import { ChatSideBar } from "./components";


// export default function Chat() {
//   const [message, setMessage] = useState<string>("");
//   const [chats, setChats] = useState<ChatThread[]>([]);
//   const [created, setCreated] = useState<boolean>(false);
//   const { getThreads } = useUserThreads();
//   const [token, setToken] = useState<string | undefined>("")
//   const { user } = useAuth();

//   useEffect(() => {
//     const getToken = async () => {
//       const t = await user?.getIdToken()
//       setToken(t)

//     }
//     getToken()
//   }, [user]
//   )



//   // Context
//   const { sources, setSources, agent, setAgent, threadId, setThreadId } =
//     UseLectureChatContext();
//   const pendingMessage = useRef<string | null>(null);
//   const generateThread = useGenerateThread();
//   // Fetch all the users previos convos
//   useEffect(() => {
//     const fetch = async () => {
//       const oldThreads = await getThreads();
//       setChats(
//         oldThreads.map((t) => ({ title: t.title, id: t.id }) as ChatThread),
//       );
//     };
//     fetch();
//   }, [user]);

//   const handleNewChats = async () => {
//     stream.stop?.();
//     setThreadId(null);
//     setCreated(false);
//   };

//   const stream = useStream({
//     assistantId: agent,
//     apiUrl: streamURL,
//     apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
//     threadId: threadId ?? undefined,

//     onThreadId: async (id: string) => {
//       if (created) return;
//       setCreated(true);

//       const threadData: ThreadCreate = {
//         agent,
//         thread_id: id,
//         course_id: null,
//         user_id: null,
//         title: pendingMessage.current ?? "New Chat",
//       };
//       const response = await generateThread(threadData);
//       setThreadId(id);
//       setChats((prev) => [
//         { id, title: response.title ?? "New Chat" },
//         ...prev,
//       ]);
//     },
//   });

//   const handleSubmit = async () => {
//     try {
//       if (!message.trim()) {
//         return;
//       }

//       if (!threadId) {
//         // First message so store it and let onThreadId handle saving it
//         pendingMessage.current = message;
//       } else {
//         // thread already exists, save directly
//         await api.post(`/threads/${threadId}/messages`, {
//           role: "human",
//           content: message,
//         });
//       }

//       stream.submit({
//         messages: [{ content: message, type: "human" }],
//       });
//       setMessage("");
//     } catch (error: any) {
//       console.log("Error", error);
//     }
//   };

//   useEffect(() => {
//     if (!stream.isLoading && stream.messages.length > 0 && threadId) {
//       const lastMessage = stream.messages[stream.messages.length - 1];
//       if (lastMessage.type === "ai") {
//         api.post(`/threads/${threadId}/messages`, {
//           role: "ai",
//           content: String(lastMessage.content),
//         });
//       }
//     }
//   }, [stream.isLoading]);

//   useEffect(() => {
//     const last = stream.messages.at(-1);

//     if (!last) return;

//     if (last.type !== "tool" || !last.artifact) return;

//     const artifacts = (
//       Array.isArray(last.artifact)
//         ? last.artifact
//         : Object.values(last.artifact)
//     ) as LectureArtifact[];

//     setSources(artifacts);
//   }, [stream.messages]);

//   return (
//     <div className="flex flex-col max-w-6xl mx-auto h-[80vh]">
//       {/* Header */}
//       <div className="flex items-center justify-between mb-3">
//         <h2 className="text-lg font-semibold text-slate-800">
//           Lecture Tutor: Thread {threadId}
//         </h2>

//         <DropDown
//           options={["agent_me135", "agent_me118"]}
//           selected={agent}
//           label="Select Course"
//           setSelected={(v) => setAgent(v as ValidAgent)}
//         />
//       </div>
//       <div className="flex flex-1 min-h-0 items-stretch">
//         <ChatSideBar
//           chats={chats}
//           activeChatId={threadId ?? undefined}
//           onSelectChat={(id) => {
//             setThreadId(id);
//           }}
//           onNewChat={handleNewChats}
//         />
//         <div className="flex-1 min-w-0">
//           {/* Chat Container */}
//           <ChatContainer className="flex w-full h-full">
//             {/* Messages */}
//             <div className="flex-1 h-full overflow-y-auto px-6 py-5 space-y-3 bg-slate-50">
//               {stream.messages.map((msg, idx) => (
//                 <ChatMessage key={idx} message={msg} id={idx} />
//               ))}

//               {stream.isLoading && (
//                 <div className="text-sm text-slate-400 animate-pulse">
//                   Assistant is thinking...
//                 </div>
//               )}

//               {sources.length > 0 && (
//                 <div className="pt-2">
//                   <SourceSection sources={sources} />
//                 </div>
//               )}
//             </div>

//             {/* Input */}

//             <div className="w-full m-2 p-1">
//               <ChatInput
//                 value={message}
//                 setValue={setMessage}
//                 onSubmit={() => {
//                   handleSubmit();
//                 }}
//               />
//             </div>
//           </ChatContainer>
//         </div>
//       </div>
//     </div>
//   );
// }


type ChatSessionProps = {
  onNewChat: () => void;
  token: string;
};

export function ChatSession({ onNewChat, token }: ChatSessionProps) {
  const threadId = useChatContext((s) => s.theadId);
  const createThread = useChatContext((s) => s.createdThread);
  const setThreadId = useChatContext((s) => s.setThreadId);

  const stream = useStream({
    threadId: threadId || null,
    apiUrl: streamURL,
    assistantId: "agent_me116",
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    onThreadId: async (id: string) => {
      const data: ThreadCreate = {
        thread_id: id
      };
      const created = await createThread(token, data);
      setThreadId(created.id);
    },
  });

  const handleSubmit = async (
    text: string,
    images?: string[] | null | undefined,
  ) => {
    type ContentItem =
      | { type: "text"; text: string }
      | { type: "image_url"; image_url: { url: string } };

    const content: ContentItem[] = [{ type: "text", text }];

    if (images && images.length > 0) {
      const b64 = await blobURLtoBase64(images[0]);
      content.push({
        type: "image_url",
        image_url: { url: b64 },
      });
    }

    stream.submit({
      messages: [
        {
          role: "human",
          content,
        },
      ],
    });
  };

  return (
    <ChatContainer
      size="lg"
      onNewChat={onNewChat}
      scrollTrigger={stream.messages.length}
      input={
        <ChatInput
          handleSubmit={handleSubmit}
          disabled={stream.isLoading}
          multiModal={true}
        />
      }
    >
      <MathJax dynamic>
        {stream.messages.map((msg) => {
          if (msg.type === "human") {
            return <HumanBubble key={msg.id} msg={msg as HumanMessage} />;
          }
          if (msg.type === "ai") {
            return <AIBubble key={msg.id} msg={msg as AIMessage}></AIBubble>;
          }
          if (msg.type === "tool") {
            return <RenderToolCalls key={msg.id} msg={msg as ToolMessage} />;
          }

          return null;
        })}
      </MathJax>
    </ChatContainer>
  );
}

export default function Chat() {
  const { user } = useAuth();
  const threadId = useChatContext((s) => s.theadId);
  const setThreadId = useChatContext((s) => s.setThreadId);
  const getUserThreads = useChatContext((s) => s.getUserThreads);
  const [token, setToken] = useState<string>("");
  const [showSideBar, setShowSideBar] = useState<boolean>(true);
  const [sessionKey, setSessionKey] = useState(0);
  const [threads, setThreads] = useState<Thread[]>([]);
  const [selectedThreadId, setSelectedThreadId] = useState<string>("");

  const loadUserThreads = useCallback(
    async (authToken: string) => {
      const res = await getUserThreads(authToken);
      setThreads(res);
    },
    [getUserThreads],
  );

  useEffect(() => {
    let isMounted = true;

    const bootstrap = async () => {
      if (!user) return;
      const authToken = await user.getIdToken();
      if (!isMounted) return;

      setToken(authToken);
      await loadUserThreads(authToken);
    };

    void bootstrap();

    return () => {
      isMounted = false;
    };
  }, [user, loadUserThreads]);


  const handleNewChat = () => {
    setSelectedThreadId("");
    setThreadId(null);
    setSessionKey((k) => k + 1);
  };

  if (!token) {
    return (
      <div className="w-full rounded-lg border border-border bg-surface p-4 text-sm text-text-muted shadow-soft">
        Loading chat...
      </div>
    );
  }

  return (
    <section className="mx-auto flex w-full max-w-7xl gap-3 rounded-xl border border-border bg-surface p-3 shadow-soft backdrop-blur">
      <aside
        className={`flex flex-col border-r overflow-x-clip border-border pr-3 transition-all duration-base ease-base ${showSideBar ? "w-72 gap-3" : "w-11 gap-0"
          }`}
      >
        <button
          type="button"
          aria-label={showSideBar ? "Close sidebar" : "Open sidebar"}
          onClick={() => setShowSideBar((prev) => !prev)}
          className="self-end rounded-md border border-border bg-surface p-2 text-text-muted transition-colors duration-base ease-base hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
        >
          <GiHamburgerMenu />
        </button>

        {showSideBar && <ChatSideBar chats={threads} activeChatId={threadId} onSelectChat={setThreadId} />}

      </aside>

      <div className="min-w-0 flex-1 pl-1 sm:pl-2">
        <ChatSession key={sessionKey} onNewChat={handleNewChat} token={token} />
      </div>
    </section>
  );
}
