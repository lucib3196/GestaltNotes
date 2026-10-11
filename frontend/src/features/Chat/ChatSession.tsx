import { useStream } from "@langchain/langgraph-sdk/react";
import { MathJax } from "better-react-mathjax";
import { streamURL } from "../../config/api";
import ChatContainer from "./ui/layout/ChatContainer";
import ChatInput from "./ui/composer/ChatInput";
import { ChatModelPicker } from "./ui/composer/ChatModelPicker";
import { ChatSessionHeader } from "./ui/layout/ChatSessionHeader";
import { useChatStore } from "./instance";
import { prepareMessage } from "./utils/messageSending";
import { useCreateThread } from "./hooks/useCreateThread";
import MessageList from "./ui/messages/MessageList";
import { useEffect } from "react";
import type { Message } from "@langchain/langgraph-sdk";
import { useUpdateThread } from "./hooks/useUpdateThread";

type ChatAgentState = {
  messages: Message[];
  thread_title?: string;
};

export default function ChatSession() {
  const config = useChatStore((s) => s.config);
  const activeThreadId = useChatStore((s) => s.activeThreadId);
  const threadsById = useChatStore((s) => s.threadsById);
  const activeThread = useChatStore((s) =>
    activeThreadId ? (s.threadsById[activeThreadId] ?? null) : null,
  );
  const { updateThread } = useUpdateThread();
  const assistantId = useChatStore((s) => s.assistant.id);
  const draftText = useChatStore((s) => s.draftText);
  const setDraftText = useChatStore((s) => s.setDraftText);
  const setActiveThread = useChatStore((s) => s.selectThread);
  const upsertThread = useChatStore((s) => s.upsertThread);

  // Hooks
  const { createThread } = useCreateThread();

  const stream = useStream<ChatAgentState>({
    threadId: activeThreadId,
    apiUrl: streamURL,
    assistantId: assistantId,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    onThreadId: async (id: string) => {
      const thread = await createThread({ thread_id: id });
      upsertThread(thread);
      setActiveThread(thread.id);
    },
    onFinish: (state, run) => {
      const title = state.values.thread_title?.trim();
      const threadId = run?.thread_id;
      if (!threadId) return;
      const thread = threadsById[threadId];

      if (!title || !thread || thread.title_source !== "default") return;

      void updateThread(threadId, { title, title_source: "generated" })
        .then((updatedThread) => {
          if (updatedThread) {
            upsertThread(updatedThread);
          }
        })
        .catch((error) => {
          console.error("Could not save the conversation title", error);
        });
    },
  });

  const handleSubmit = async (text: string, images?: string[]) => {
    const content = await prepareMessage(text, images);

    stream.submit(
      {
        messages: [
          {
            type: "human",
            content,
          },
        ],
      },
      {
        context: config,
      },
    );
  };
  useEffect(() => {
    const handleExternalMessage = async () => {
      if (!draftText) return;
      const content = await prepareMessage(draftText);
      stream.submit({
        messages: [
          {
            type: "human",
            content,
            additional_kwargs: {
              internal: true,
            },
          },
        ],
      }, { context: config });
      setDraftText("");
    };
    void handleExternalMessage();
  }, [draftText]);

  const visibleMessages = stream.messages.filter(
    (message) =>
      !(
        message.type === "human" && message.additional_kwargs?.internal === true
      ),
  );

  return (
    <section className="flex flex-col h-full py-2 min-h-0 min-w-0 bg-inherit">
      <ChatSessionHeader thread={activeThread} />
      <div className="min-h-0 min-w-0 flex-1">
        <ChatContainer
          bordered={false}
          scrollTrigger={stream.messages.length}
          starters={null}
          input={
            <ChatInput
              handleSubmit={handleSubmit}
              disabled={stream.isLoading}
              multiModal={true}
              toolbar={<ChatModelPicker disabled={stream.isLoading} />}
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
