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
import { useEffect, useState } from "react";
import type { Message } from "@langchain/langgraph-sdk";
import { useUpdateThread } from "./hooks/useUpdateThread";

type ChatAgentState = {
  messages: Message[];
  thread_title?: string;
};

function getProgressMessage(event: unknown): string | null {
  if (
    typeof event !== "object" ||
    event === null ||
    !("type" in event) ||
    event.type !== "progress" ||
    !("message" in event) ||
    typeof event.message !== "string"
  ) {
    return null;
  }

  return event.message;
}

export default function ChatSession() {
  const [progress, setProgress] = useState<string | null>(null);
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
    onCustomEvent: (event) => {
      const message = getProgressMessage(event);
      if (message !== null) setProgress(message);
    },
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

  useEffect(() => {
    setProgress(null);
  }, [activeThreadId]);

  const handleSubmit = async (text: string, images?: string[]) => {
    const content = await prepareMessage(text, images);

    setProgress(null);
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
        streamMode: ["messages", "updates", "custom"],
      },
    );
  };
  useEffect(() => {
    const handleExternalMessage = async () => {
      if (!draftText) return;
      const content = await prepareMessage(draftText);
      setProgress(null);
      stream.submit(
        {
          messages: [
            {
              type: "human",
              content,
              additional_kwargs: {
                internal: true,
              },
            },
          ],
        },
        { context: config, streamMode: ["messages", "updates", "custom"] },
      );
      setDraftText("");
    };
    void handleExternalMessage();
  }, [draftText]);

  const visibleMessages = stream.messages.filter((message) => {
    if (
      message.type === "human" &&
      message.additional_kwargs?.internal === true
    ) {
      return false;
    }

    if (message.type === "ai") {
      const metadata =
        stream.getMessagesMetadata(message)?.streamMetadata;

      // Internal model calls made while a tool is running.
      if (metadata?.langgraph_node === "tools") {
        return false;
      }
    }

    return true;
  });

  return (
    <>
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
            {stream.isLoading && (
              <div
                role="status"
                aria-live="polite"
                className="mx-auto w-full max-w-4xl px-4 py-3 text-sm text-base-content/70"
              >
                {progress ?? "Working…"}
              </div>
            )}
          </MathJax>
        </ChatContainer>
      </div>
</>
  );
}
