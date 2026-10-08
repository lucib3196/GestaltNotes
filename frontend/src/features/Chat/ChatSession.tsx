import { useStream } from "@langchain/langgraph-sdk/react";
import { MathJax } from "better-react-mathjax";
import { AIMessage, HumanMessage } from "langchain";
import { streamURL } from "../../config/api";
import { AIBubble, HumanBubble } from "./components/ChatMessage";
import { ChatContainer, ChatInput } from "./components";

import { useChatStore } from "./instance";
import { prepareMessage } from "./utils";
import { useCreateThread } from "./hooks/useCreateThread";

export default function ChatSession() {
  const activeThreadId = useChatStore((s) => s.activeThreadId);
  const assistantId = useChatStore((s) => s.assistant.id);
  const setActiveThread = useChatStore((s) => s.selectThread);


  console.log("Current active thread", activeThreadId)

  // Hooks
  const { createThread } = useCreateThread();

  const stream = useStream({
    threadId: activeThreadId,
    apiUrl: streamURL,
    assistantId: assistantId,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    onThreadId: async (id: string) => {
      const thread = await createThread({ thread_id: id });
      setActiveThread(thread.id);
    },
  });

  const handleSubmit = async (text: string, images?: string[]) => {
    const content = await prepareMessage(text, images);

    stream.submit({
      messages: [
        {
          role: "human",
          content,
        },
      ],
    });
  };
  // useEffect(() => {
  //   if (!currentThread) return;
  //   if (currentThread) {
  //     clearWorkspaceItems();
  //   }
  // }, [currentThread?.id]);

  // useEffect(() => {
  //   stream.messages.forEach((msg) => {
  //     if (msg.type === "tool") {
  //       appendToolMessage(msg as ToolMessage);
  //     }
  //   });
  // }, [stream.messages, appendToolMessage, currentThread?.id]);

  // useEffect(() => {
  //   if (!externalMessage) return;
  //   handleSubmit(externalMessage);
  //   setExternalMessage(null);
  //   // handleSubmit(externalMessage);
  // }, [externalMessage]);

  return (
    <section className="flex h-full min-h-0 flex-col rounded-lg border border-border bg-surface-strong">
      <div className="shrink-0  border-border px-3 py-2 sm:px-4">
        {/* <ChatSessionHeader thread={currentThread} /> */}
      </div>
      <div className="min-h-0 flex-1">
        <ChatContainer
          size="lg"
          bordered={false}
          scrollTrigger={stream.messages.length}
          starters={null}
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
                return (
                  <AIBubble key={msg.id} msg={msg as AIMessage}></AIBubble>
                );
              }
              return null;
            })}
          </MathJax>
        </ChatContainer>
      </div>
    </section>
  );
}
