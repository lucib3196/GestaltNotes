import clsx from "clsx";
import { useState } from "react";
import { BsLayoutSidebarReverse } from "react-icons/bs";
import { useGetThreads } from "../../hooks/useGetThreads";
import { useChatStore } from "../../instance";
import ThreadItem from "./ThreadItem";
import ToolBar from "./ToolBar";

const containerStyle =
  "flex h-full min-h-svh shrink-0 flex-col gap-3 overflow-hidden rounded-xl border border-border shadow-sm";

export default function ChatSideBar() {
  const [collapsed, setCollapsed] = useState(false);
  const { threads, loading, error } = useGetThreads();
  const selectedThread = useChatStore((s) => s.activeThreadId);
  const selectThread = useChatStore((s) => s.selectThread);

  return (
    <aside
      aria-label="Chat sidebar"
      className={clsx(
        containerStyle,
        collapsed
          ? "w-14 items-center bg-surface p-2"
          : "w-72 bg-surface-strong p-3",
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

      <ToolBar collapsed={collapsed} />

      {!collapsed && (
        <nav
          aria-label="Chat threads"
          aria-busy={loading}
          className="min-h-0 flex-1 space-y-1 overflow-y-auto p-1"
        >
          <p>Recent</p>
          {loading ? (
            <p role="status" className="px-3 py-6 text-sm text-text-soft">
              Loading chats...
            </p>
          ) : error ? (
            <p role="alert" className="px-3 py-6 text-sm text-red-500">
              Failed to load chats
            </p>
          ) : threads.length === 0 ? (
            <p className="px-3 py-6 text-center text-sm text-text-soft">
              No chats yet
            </p>
          ) : (
            threads.map((thread) => (
              <ThreadItem
                key={thread.id}
                thread={thread}
                selected={thread.id === selectedThread}
                onSelect={selectThread}
              />
            ))
          )}
        </nav>
      )}
    </aside>
  );
}
