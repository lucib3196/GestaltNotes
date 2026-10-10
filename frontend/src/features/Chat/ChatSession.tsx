import { useStream } from "@langchain/langgraph-sdk/react";
import { MathJax } from "better-react-mathjax";
import { streamURL } from "../../config/api";
import ChatContainer from "./ui/layout/ChatContainer";
import ChatInput from "./ui/composer/ChatInput";
import { ChatSessionHeader } from "./ui/layout/ChatSessionHeader";
import { useChatStore } from "./instance";
import { prepareMessage } from "./utils/messageSending";
import { useCreateThread } from "./hooks/useCreateThread";
import MessageList from "./ui/messages/MessageList";
import { useEffect } from "react";
export default function ChatSession() {
  const activeThreadId = useChatStore((s) => s.activeThreadId);
  const activeThread = useChatStore((s) =>
    activeThreadId ? (s.threadsById[activeThreadId] ?? null) : null,
  );
  const assistantId = useChatStore((s) => s.assistant.id);
  const draftText = useChatStore((s) => s.draftText);
  const setDraftText = useChatStore((s) => s.setDraftText);
  const setActiveThread = useChatStore((s) => s.selectThread);
  const upsertThread = useChatStore((s) => s.upsertThread);

  // Hooks
  const { createThread } = useCreateThread();

  const stream = useStream({
    threadId: activeThreadId,
    apiUrl: streamURL,
    assistantId: assistantId,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    onThreadId: async (id: string) => {
      const thread = await createThread({ thread_id: id });
      upsertThread(thread);
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
  useEffect(() => {
    const handleExternalMessage = async () => {
      if (!draftText) return;
      const content = await prepareMessage(draftText);
      stream.submit({
        messages: [
          {
            role: "human",
            content,
            additional_kwargs: {
              internal: true,
              purpose: "quiz_review",
            },
          },
        ],
      });
      setDraftText("");
    };
    void handleExternalMessage();
  }, [draftText]);

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

  const visibleMessages = stream.messages.filter(
    (message) =>
      !(
        message.type === "human" &&
        message.additional_kwargs?.internal === true
      ),
  );

  return (
    <section className="flex h-full min-h-0 flex-col rounded-lg border border-border bg-surface-strong">
      <ChatSessionHeader thread={activeThread} />
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
            <MessageList messages={visibleMessages} />
          </MathJax>
        </ChatContainer>
      </div>
    </section>
  );
}
