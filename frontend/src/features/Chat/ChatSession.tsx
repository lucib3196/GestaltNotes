import { useStream } from "@langchain/langgraph-sdk/react";
import { MathJax } from "better-react-mathjax";
import { AIMessage, HumanMessage, ToolMessage } from "langchain";
import { useEffect } from "react";

import { streamURL } from "../../config/api";
import { ChatContainer, ChatInput, ConversationStarters } from "./components";
import { AIBubble, HumanBubble } from "./components/ChatMessage";
import { useChatContext } from "./instance";
import type { ConversationStarter } from "./instance/types";
import { blobURLtoBase64 } from "./utils";
import { ChatSessionHeader } from "./components/ChatSessionHeader";

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
  token: string;
};

const starters: ConversationStarter[] = [
  {
    id: "ht-quiz",
    label: "Generate Heat Transfer Quiz",
    message: "Generate Heat Transfer Quiz",
    description: "Create a concise MCQ set from current heat transfer context.",
  },
  {
    id: "ht-summary",
    label: "Summarize Heat Transfer Concepts",
    message: "Summarize Heat Transfer Concepts",
    description: "Summarize key heat transfer ideas discussed so far.",
  },
  {
    id: "ht-fourier",
    label: "Explain Fourier’s Law",
    message: "Explain Fourier’s Law",
    description: "Give a concise explanation of Fourier’s law of heat conduction with a simple example.",
  },

];

export default function ChatSession({ token }: ChatSessionProps) {
  const threadId = useChatContext((s) => s.theadId);
  const assistantId = useChatContext((s) => s.assistantId)
  const onThreadId = useChatContext((s) => s.onThreadId)
  const appendToolMessage = useChatContext((s) => s.appendToolMessage)


  const stream = useStream({
    threadId: threadId || null,
    apiUrl: streamURL,
    assistantId: assistantId,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    onThreadId: async (id: string) => {
      await onThreadId(id, token)
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


  useEffect(() => {
    stream.messages.forEach((msg) => {
      if (msg.type === "tool") {
        appendToolMessage(msg as ToolMessage);
      }
    });
  }, [stream.messages, appendToolMessage]);

  const generateQuizToolBar = (
    <div className="flex items-center">
      <button
        type="button"
        onClick={() => {
          void handleSubmit("Generated a mcq_question with 3 questions");
        }}
        disabled={stream.isLoading || stream.messages.length < 1}
        className="rounded-md bg-blue-300 px-3.5 py-2.5 text-sm font-semibold text-bg transition-all duration-base ease-base hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Generate Quiz
      </button>
    </div>
  );
  return (
    <section className="flex h-full min-h-0 flex-col rounded-lg border border-border bg-surface-strong">
      <div className="shrink-0  border-border px-3 py-2 sm:px-4">
        <ChatSessionHeader />
      </div>
      <div className="min-h-0 flex-1">
        <ChatContainer
          size="lg"
          bordered={false}
          scrollTrigger={stream.messages.length}
          starters={
            stream.messages.length === 0 ? (
              <ConversationStarters
                starters={starters}
                disabled={stream.isLoading}
                onSelectStarter={(starter) => {
                  void handleSubmit(starter.message);
                }}
              />
            ) : null
          }
          input={
            <ChatInput
              handleSubmit={handleSubmit}
              disabled={stream.isLoading}
              multiModal={true}
              toolbar={generateQuizToolBar}
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
              return null;
            })}
          </MathJax>
        </ChatContainer>
      </div>
    </section>
  );
}
