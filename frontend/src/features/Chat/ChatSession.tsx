import { useStream } from "@langchain/langgraph-sdk/react";
import { MathJax } from "better-react-mathjax";
import { AIMessage, HumanMessage, ToolMessage } from "langchain";
import { useEffect } from "react";

import { streamURL } from "../../config/api";
import { ChatContainer, ChatInput, } from "./components";
import { AIBubble, HumanBubble } from "./components/ChatMessage";
import { useChatContext } from "./instance";
import ConversationStarters from "../ConversationStarters/components/ConverstationStarter";
import { useThreadStore } from "./instance/store";
import { blobURLtoBase64 } from "./utils";
import { ChatSessionHeader } from "./components/ChatSessionHeader";
import { useGetThread } from "./hooks/hooks";

import { useGenerateThread } from "./hooks/hooks";



export default function ChatSession() {


  // State
  const currentThread = useThreadStore((s) => s.thread);

  const assistantId = useChatContext((s) => s.assistantId);
  const appendToolMessage = useChatContext((s) => s.appendToolMessage);

  // Hooks
  const { generateThread } = useGenerateThread();
  const { loading, error } = useGetThread();

  const stream = useStream({
    threadId: currentThread?.id || null,
    apiUrl: streamURL,
    assistantId: assistantId,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    onThreadId: async (id: string) => {
      generateThread({
        thread_id: id,
      });
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
            stream.messages.length === 0 ? <ConversationStarters onSelect={(v) => handleSubmit(v)} /> : null
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
