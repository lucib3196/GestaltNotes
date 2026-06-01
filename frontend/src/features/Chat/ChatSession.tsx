import { useStream } from "@langchain/langgraph-sdk/react";
import { MathJax } from "better-react-mathjax";
import { AIMessage, HumanMessage, ToolMessage } from "langchain";
import { useEffect } from "react";
import { streamURL } from "../../config/api";
import ConversationStarters from "../ConversationStarters/components/ConverstationStarter";
import { useWorkspaceStore } from "../Tools/instance/store";
import { AIBubble, HumanBubble } from "./components/ChatMessage";
import { ChatSessionHeader } from "./components/ChatSessionHeader";
import { ChatContainer, ChatInput } from "./components";
import { useGenerateThread, useGetThread } from "./hooks/hooks";

import { useThreadStore, useChatStore } from "./instance/store";
import { prepareMessage } from "./utils";

export default function ChatSession() {
  // State
  const currentThread = useThreadStore((s) => s.thread);
  const assistantId = useChatStore((s) => s.assistantId);
  const externalMessage = useChatStore((s) => s.externalMessage);
  const setExternalMessage = useChatStore((s) => s.setExternalMessage)
  const appendToolMessage = useWorkspaceStore((s) => s.appendToolMessage);
  const clearWorkspaceItems = useWorkspaceStore((s) => s.clearWorkspace);
  // Hooks
  const { generateThread } = useGenerateThread();
  const { loading, error } = useGetThread();




  const stream = useStream({
    threadId: currentThread?.id || null,
    apiUrl: streamURL,
    assistantId: assistantId,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    onThreadId: async (id: string) => {
      await generateThread({
        thread_id: id,
      });

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
  useEffect(() => {
    if (!currentThread) return;
    if (currentThread) {
      clearWorkspaceItems();
    }
  }, [currentThread?.id]);

  useEffect(() => {
    stream.messages.forEach((msg) => {
      if (msg.type === "tool") {
        appendToolMessage(msg as ToolMessage);
      }
    });
  }, [stream.messages, appendToolMessage, currentThread?.id]);

  useEffect(() => {
    if (!externalMessage) return;
    handleSubmit(externalMessage)
    setExternalMessage(null)
    // handleSubmit(externalMessage);
  }, [externalMessage]);


  if (loading) return <div>Loading</div>;
  if (error) return <div>Error</div>;

  return (
    <section className="flex h-full min-h-0 flex-col rounded-lg border border-border bg-surface-strong">
      <div className="shrink-0  border-border px-3 py-2 sm:px-4">
        <ChatSessionHeader thread={currentThread} />
      </div>
      <div className="min-h-0 flex-1">
        <ChatContainer
          size="lg"
          bordered={false}
          scrollTrigger={stream.messages.length}
          starters={
            stream.messages.length === 0 ? (
              <ConversationStarters onSelect={(v) => handleSubmit(v)} />
            ) : null
          }
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
