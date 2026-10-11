import clsx from "clsx";
import { useState } from "react";
import { BsLayoutSidebarReverse } from "react-icons/bs";
import { useGetThreads } from "../../hooks/useGetThreads";
import { useChatStore } from "../../instance";
import ThreadList from "./ThreadList";
import ChatSidebarToolbar from "./ChatSidebarToolbar";

const containerStyle =
  "flex h-full min-h-0 shrink-0 flex-col gap-2 overflow-hidden border-0 bg-inherit shadow-none sm:gap-3 ";

const collapsedStyle = "w-10 items-center p-1 sm:w-14 md:w-12  sm:p-2 ";

const expandedStyle = "w-60 p-2 sm:w-72 sm:p-3 ";

export default function ChatSidebar() {
  const [collapsed, setCollapsed] = useState(() =>
    typeof window !== "undefined"
      ? window.matchMedia("(max-width: 1023px)").matches
      : false,
  );
  const { threads, loading, error, refetch } = useGetThreads();
  const selectedThread = useChatStore((s) => s.activeThreadId);
  const removeThread = useChatStore((s) => s.removeThread);
  const selectThread = useChatStore((s) => s.selectThread);

  return (
    <aside
      aria-label="Chat sidebar"
      className={clsx(
        containerStyle,
        collapsed ? collapsedStyle : expandedStyle,
      )}
    >
      <div className="flex w-full items-center justify-between">
        {!collapsed && (
          <h2 className="text-xs font-semibold uppercase tracking-widest text-text-soft">
            Chats
          </h2>
        )}
        <button
          type="button"
          onClick={() => setCollapsed((value) => !value)}
          aria-label={
            collapsed ? "Expand chat sidebar" : "Collapse chat sidebar"
          }
          aria-expanded={!collapsed}
          className="inline-flex h-9 w-9 items-center justify-center rounded-md text-text-soft hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
        >
          <BsLayoutSidebarReverse aria-hidden="true" />
        </button>
      </div>

      <ChatSidebarToolbar collapsed={collapsed} />

      {!collapsed && (
        <ThreadList
          threads={threads}
          loading={loading}
          error={error}
          selectedThreadId={selectedThread}
          onSelect={selectThread}
          onRenamed={refetch}
          onDeleted={(id) => {
            removeThread(id);
            refetch();
          }}
          onRetry={refetch}
        />
      )}
    </aside>
  );
}
