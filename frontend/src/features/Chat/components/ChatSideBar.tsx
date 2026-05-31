import clsx from "clsx";
import ThreadBubble from "./ThreadBubble";
import type { ThreadUpdate } from "../../../services/chat/types";
import ChatActions from "./ChatActions";
import { useThreadStore } from "../instance/store";
import { useEffect } from "react";
import { useGetThreads } from "../hooks/hooks";
const sidebarBaseStyle =
  "flex h-full m-2 flex-col rounded-lg border border-border bg-surface-strong p-2";

export type ChatSideBarProps = React.HTMLAttributes<HTMLDivElement> & {
  activeChatId?: string | null;
  onSelectChat: (id: string | null, token: string | null) => void;
  onNewChat?: () => Promise<void>;
  onThreadUpdate?: (id: string, data: ThreadUpdate) => Promise<void>;
};

export default function ChatSideBar({ className, ...rest }: ChatSideBarProps) {
  const threadId = useThreadStore((s) => s.threadId);
  const setThreadId = useThreadStore((s) => s.setThreadId);
  const allThreads = useThreadStore((s) => s.threads);
  const {
    getThreads,
    loading,
    error,
  } = useGetThreads();


  useEffect(() => {
    getThreads();
  }, [getThreads]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className={clsx(sidebarBaseStyle, className)} {...rest}>
      {/* Header */}
      <div className="mb-2 flex flex-col  items-center justify-between  px-2 pb-3 pt-2">
        <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-text-soft">
          Chats
        </h2>
        <ChatActions />
      </div>

      {/* Chat List */}
      <nav className="flex-1 space-y-1 overflow-y-auto px-1 pb-1">
        {allThreads.length === 0 ? (
          <p className="px-3 py-8 text-center text-sm text-text-soft">
            No chats yet
          </p>
        ) : (
          allThreads.map((t) => {
            return (
              <ThreadBubble
                thread={t}
                selected={t.id === threadId}
                onClick={() => {
                  setThreadId(t.id);
                }}
              />
            );
          })
        )}
      </nav>
    </div>
  );
}
