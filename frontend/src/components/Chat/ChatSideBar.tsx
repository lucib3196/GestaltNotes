import clsx from "clsx";

export type Chat = {
  id: string;
  title: string;
  preview?: string;
  timestamp?: string;
  unread?: boolean;
};

export type ChatSideBarProps = React.HTMLAttributes<HTMLDivElement> & {
  chats: Chat[];
  activeChatId?: string;
  onSelectChat: (id: string) => void;
  onNewChat?: () => void;
};

const sidebarBaseStyle =
  "flex flex-col h-full w-64 bg-slate-50 border-r border-slate-200 shrink-0";

const chatItemStyle =
  "w-full text-left px-4 py-3 rounded-lg transition-colors duration-150 hover:bg-slate-200 focus:outline-none focus:ring-2 focus:ring-slate-400";

const chatItemActiveStyle = "bg-slate-200 font-medium";

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
      <div className="flex items-center justify-between px-4 py-4 border-b border-slate-200">
        <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wider">
          Chats
        </h2>
        {onNewChat && (
          <button
            onClick={onNewChat}
            className="text-slate-500 hover:text-slate-900 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-slate-400 rounded"
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
      <nav className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
        {chats.length === 0 ? (
          <p className="px-4 py-6 text-sm text-slate-400 text-center">
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
                <span className="truncate text-sm text-slate-800">
                  {chat.title}
                </span>
                <div className="flex items-center gap-1 shrink-0">
                  {chat.unread && (
                    <span className="h-2 w-2 rounded-full bg-blue-500" aria-label="Unread" />
                  )}
                  {chat.timestamp && (
                    <span className="text-xs text-slate-400">{chat.timestamp}</span>
                  )}
                </div>
              </div>

              {/* Preview row */}
              {chat.preview && (
                <p className="mt-0.5 truncate text-xs text-slate-400">
                  {chat.preview}
                </p>
              )}
            </button>
          ))
        )}
      </nav>
    </div>
  );
}