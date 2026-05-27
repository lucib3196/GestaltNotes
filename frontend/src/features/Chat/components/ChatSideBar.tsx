import clsx from "clsx";
import type { Thread } from "../../../services";

export type ChatSideBarProps = React.HTMLAttributes<HTMLDivElement> & {
  chats: Thread[];
  activeChatId?: string | null;
  onSelectChat: (id: string | null) => void;
  onNewChat?: () => Promise<void>;
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
  ...rest
}: ChatSideBarProps) {

  return (
    <div className={clsx(sidebarBaseStyle, className)} {...rest}>

      {/* Header */}
      <div className="mb-2 flex items-center justify-between  px-2 pb-3 pt-2">
        <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-text-soft">
          Chats
        </h2>
        {onNewChat && (
          <button
            type="button"
            onClick={onNewChat}
            className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-border bg-surface text-text-muted transition-all duration-base ease-base hover:border-border-strong hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
            aria-label="New chat"
          >
            {/* Pencil / compose icon */}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
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
          </button>
        )}
      </div>

      {/* Chat List */}
      <nav className="flex-1 space-y-1 overflow-y-auto px-1 pb-1">
        {chats.length === 0 ? (
          <p className="px-3 py-8 text-center text-sm text-text-soft">
            No chats yet
          </p>
        ) : (
          chats.map((chat) => (
            <button
              key={chat.id}
              onClick={() => onSelectChat(chat.id)}
              className={clsx(
                chatItemStyle,
                chat.id === activeChatId && chatItemActiveStyle
              )}
              aria-current={chat.id === activeChatId ? "page" : undefined}
            >
              {/* Title row */}
              <div className="flex items-center justify-between gap-2">
                <span className="truncate text-sm text-text">
                  {chat.title ?? "New Chat"}
                </span>
              </div>
            </button>
          ))
        )}
      </nav>
    </div>
  );
}
