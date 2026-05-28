import clsx from "clsx";
import type { Thread } from "../../../services";
import { useState } from "react";
import { MdOutlineDriveFileRenameOutline } from "react-icons/md";
import type { ThreadUpdate } from "../../../services/chat/types";


export type ChatSideBarProps = React.HTMLAttributes<HTMLDivElement> & {
  chats: Thread[];
  activeChatId?: string | null;
  onSelectChat: (id: string | null, token: string | null) => void;
  onNewChat?: () => Promise<void>;
  onThreadUpdate?: (id: string, data: ThreadUpdate) => Promise<void>;
};

const sidebarBaseStyle =
  "flex h-full m-2 flex-col rounded-lg border border-border bg-surface-strong p-2";

const chatItemStyle =
  "w-full rounded-md border border-transparent px-3 py-2.5 text-left transition-all duration-base ease-base hover:border-border hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60";

const chatItemActiveStyle =
  "border-border bg-surface text-text shadow-soft";

export default function ChatSideBar({
  chats,
  activeChatId,
  onSelectChat,
  onNewChat,
  className,
  onThreadUpdate,
  ...rest
}: ChatSideBarProps) {
  const [editingChatId, setEditingChatId] = useState<string | null>(null);
  const [draftTitle, setDraftTitle] = useState("");
  const canEditThreads = Boolean(onThreadUpdate);

  const startEditing = (thread: Thread) => {
    if (!canEditThreads) return;
    setEditingChatId(thread.id);
    setDraftTitle(thread.title ?? "New Chat");
  };

  const cancelEditing = () => {
    setEditingChatId(null);
    setDraftTitle("");
  };

  const confirmEditing = async () => {
    if (!canEditThreads || !editingChatId) return;
    const data: ThreadUpdate = {
      title: draftTitle
    }
    await onThreadUpdate?.(editingChatId, data);
    cancelEditing();
  };

  return (
    <div className={clsx(sidebarBaseStyle, className)} {...rest}>

      {/* Header */}
      <div className="mb-2 flex flex-col  items-center justify-between  px-2 pb-3 pt-2">
        <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-text-soft">
          Chats
        </h2>
        {onNewChat && (
          <button
            type="button"
            onClick={onNewChat}
            className="relative flex h-9 w-full items-center rounded-md border border-border bg-surface px-3 text-text-muted transition-all duration-base ease-base hover:border-border-strong hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
            aria-label="New chat"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="absolute left-3 h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.8}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 4H6a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2v-6M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"
              />
            </svg>

            <span className="w-full text-center">New Chat</span>
          </button>
        )}
      </div>

      {/* Chat List */}
      <nav className="flex-1 space-y-1 overflow-y-auto px-1 pb-1">
        {chats.length === 0 ? (
          <p className="px-3 py-8 text-center text-sm text-text-soft">No chats yet</p>
        ) : (
          chats.map((chat) => {
            const isActive = chat.id === activeChatId;
            const isEditing = chat.id === editingChatId;

            return (
              <button
                key={chat.id}
                onClick={() => !isEditing && onSelectChat(chat.id, null)}
                className={clsx(chatItemStyle, isActive && chatItemActiveStyle)}
                aria-current={isActive ? "page" : undefined}
              >
                <div className="flex items-center justify-between gap-2">
                  {isEditing ? (
                    <input
                      autoFocus
                      value={draftTitle}
                      className="w-full rounded bg-surface-muted px-2 py-1 text-sm text-text"
                      onChange={(e) => setDraftTitle(e.target.value)}
                      onClick={(e) => e.stopPropagation()}
                      onBlur={() => void confirmEditing()}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          e.preventDefault();
                          void confirmEditing();
                        }
                        if (e.key === "Escape") {
                          e.preventDefault();
                          cancelEditing();
                        }
                      }}
                    />
                  ) : (
                    <span className="truncate text-sm text-text">{chat.title ?? "New Chat"}</span>
                  )}

                  <button
                    type="button"
                    aria-label="Rename chat"
                    disabled={!canEditThreads}
                    className={clsx(
                      "rounded p-1 text-text-soft hover:bg-surface-muted hover:text-text disabled:cursor-not-allowed disabled:opacity-50",
                      isEditing && "text-accent"
                    )}
                    onClick={(e) => {
                      e.stopPropagation();
                      if (!canEditThreads) return;
                      if (isEditing) {
                        void confirmEditing();
                        return;
                      }
                      startEditing(chat);
                    }}
                  >
                    <MdOutlineDriveFileRenameOutline />
                  </button>
                </div>
              </button>
            );
          })
        )}
      </nav>
    </div>
  );
}
