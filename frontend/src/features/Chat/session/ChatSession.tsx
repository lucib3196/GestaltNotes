import { useEffect, useState } from "react";
import { useShallow } from "zustand/react/shallow";
import { useStream } from "@langchain/langgraph-sdk/react";
import type { Message } from "@langchain/langgraph-sdk";

import { streamURL } from "../../../config/api";
import ChatContainer from "../ui/layout/ChatContainer";
import ChatInput from "../ui/composer/ChatInput";
import {
  ChatModelPicker,
  ChatCoursePicker,
} from "../ui/composer/ChatModelPicker";
import { ChatSessionHeader } from "../ui/layout/ChatSessionHeader";
import MessageList from "../ui/messages/MessageList";
import { useChatStore } from "../instance";
import { prepareMessage } from "../utils/messageSending";
import { useCreateThread } from "../hooks/useCreateThread";
import { useUpdateThread } from "../hooks/useUpdateThread";
import { ConversationStarter } from "../ui/starter/ConversationStarter";
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
  const {
    config,
    activeThreadId,
    threadsById,
    assistant,
    draftMessage,
    setDraftMessage,
    selectThread,
    upsertThread,
  } = useChatStore(
    useShallow((s) => ({
      config: s.config,
      activeThreadId: s.activeThreadId,
      threadsById: s.threadsById,
      assistant: s.assistant,
      draftMessage: s.draftMessage,
      setDraftMessage: s.setDraftMessage,
      selectThread: s.selectThread,
      upsertThread: s.upsertThread,
    })),
  );

  const activeThread = activeThreadId
    ? (threadsById[activeThreadId] ?? null)
    : null;

  const { updateThread } = useUpdateThread();

  // Hooks
  const { createThread } = useCreateThread();

  const stream = useStream<ChatAgentState>({
    threadId: activeThreadId,
    apiUrl: streamURL,
    assistantId: assistant.id,
    apiKey: import.meta.env.VITE_LANGSMITH_API_KEY,
    onCustomEvent: (event) => {
      const message = getProgressMessage(event);
      if (message !== null) setProgress(message);
    },
    onThreadId: async (id: string) => {
      const thread = await createThread({ thread_id: id });
      upsertThread(thread);
      selectThread(thread.id);
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
      if (!draftMessage?.text) return;
      const content = await prepareMessage(draftMessage.text);
      setProgress(null);
      stream.submit(
        {
          messages: [
            {
              type: "human",
              content,
              additional_kwargs: {
                internal: draftMessage.internal,
              },
            },
          ],
        },
        { context: config, streamMode: ["messages", "updates", "custom"] },
      );
      setDraftMessage(null);
    };
    void handleExternalMessage();
  }, [draftMessage]);

  const visibleMessages = stream.messages.filter((message) => {
    if (
      message.type === "human" &&
      message.additional_kwargs?.internal === true
    ) {
      return false;
    }

    if (message.type === "ai") {
      const metadata = stream.getMessagesMetadata(message)?.streamMetadata;

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
          starters={
            stream.messages.length > 1 ? null : (
              <div className="flex flex-row wrap gap-2">
                {[
                  "Explain a key concept from my course with a simple example.",
                  "Create 5 multiple-choice questions to check my understanding.",
                  "Make 10 flashcards covering the main ideas from my lectures.",
                  "Show me a diagram connecting the key concepts in this topic.",
                ].map((starter) => (
                  <ConversationStarter key={starter} value={starter} />
                ))}
              </div>
            )
          }
          input={
            <ChatInput
              handleSubmit={handleSubmit}
              disabled={stream.isLoading}
              multiModal={true}
              toolbar={
                <div className="flex flex-row gap-2">
                  <ChatModelPicker disabled={stream.isLoading} />{" "}
                  <ChatCoursePicker disabled={stream.isLoading} />
                </div>
              }
            />
          }
        >
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
        </ChatContainer>
      </div>
    </>
  );
}
