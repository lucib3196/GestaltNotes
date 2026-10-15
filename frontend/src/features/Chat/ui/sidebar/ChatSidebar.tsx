import clsx from "clsx";
import { useState } from "react";
import { BsLayoutSidebarReverse } from "react-icons/bs";
import { useGetThreads } from "../../hooks/useGetThreads";
import { useChatStore } from "../../instance";
import ThreadList from "./ThreadList";
import ChatSidebarToolbar from "./ChatSidebarToolbar";

const containerStyle =
  "flex h-full min-h-0 shrink-0 flex-col gap-4 overflow-hidden border-r border-border bg-inherit shadow-none";

const collapsedStyle = "w-12 items-center px-1 py-4 sm:w-14 sm:px-2";

const expandedStyle = "w-60 px-3 py-4 sm:w-64 sm:px-4";

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
