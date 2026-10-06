import { useState } from "react";
import { BsLayoutSidebarReverse } from "react-icons/bs";
import ThreadBubble from "../../components/ThreadBubble";
import { NewChatButton } from "../buttons/ChatActions";
import { useChatStore } from "../../instance";
import { useGetThreads } from "../../hooks/useGetThreads";

const sidebarExpandedStyle =
  "h-full w-72 min-w-72 rounded-xl border border-border bg-surface-strong p-3 shadow-sm ring-1 ring-black/5";
const sidebarCollapsedStyle = "h-full w-12 min-w-12 rounded-xl border border-border bg-surface p-2";

export default function ChatSideBar() {
  const threadId = useChatStore((s) => s.threadId);
  const setThreadId = useChatStore((s) => s.setThreadId);
  const allThreads = useChatStore((s) => s.threads);
  const [collapsed, setCollapsed] = useState<boolean>(false);
  const { loading, error } = useGetThreads();

  return (
    <aside className={collapsed ? sidebarCollapsedStyle : sidebarExpandedStyle}>
      <button
        type="button"
        onClick={() => setCollapsed((prev) => !prev)}
        className="mb-2 inline-flex h-8 w-8 items-center justify-center rounded-md border border-border text-text-soft hover:bg-surface"
        aria-label={collapsed ? "Open chat sidebar" : "Close chat sidebar"}
        aria-expanded={!collapsed}
      >
        <BsLayoutSidebarReverse />
      </button>
      {collapsed &&  <NewChatButton variant={"icon"}/>}
      

      {!collapsed && (
        <>
          <div className="mb-2 flex flex-col items-center justify-between px-1">
            <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-text-soft">
              Chats
            </h2>
            <NewChatButton />
          </div>

          {loading ? (
            <div className="mt-6 rounded-md border border-border px-3 py-2 text-sm text-text-soft">
              Loading chats...
            </div>
          ) : error ? (
            <div className="mt-6 rounded-md border border-border px-3 py-2 text-sm text-red-500">
              Failed to load chats
            </div>
          ) : (
            <nav className="flex-1 space-y-1 overflow-y-auto px-1 pb-1">
              {allThreads.length === 0 ? (
                <p className="px-3 py-8 text-center text-sm text-text-soft">
                  No chats yet
                </p>
              ) : (
                allThreads.map((t) => (
                  <ThreadBubble
                    key={t.id}
                    thread={t}
                    selected={t.id === threadId}
                    onClick={() => {
                      setThreadId(t.id);
                    }}
                  />
                ))
              )}
            </nav>
          )}
        </>
      )}
    </aside>
  );
}
