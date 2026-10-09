import clsx from "clsx";
import { useChatStore } from "../../instance";
import { useGetThreads } from "../../hooks/useGetThreads";
type NewChatButtonProps = {
  variant?: "full" | "icon";
  disabled?: boolean;
  className?: string;
};

export function NewChatButton({
  variant = "full",
  disabled = false,
  className,
}: NewChatButtonProps) {
  const startNewChat = useChatStore((s) => s.startNewChat);
  const { refetch } = useGetThreads();

  const handleClick = () => {
    startNewChat();
    refetch();
  };
  const iconOnly = variant === "icon";

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={disabled}
      aria-label="New chat"
      title={iconOnly ? "New chat" : undefined}
      className={clsx(
        "inline-flex h-9 items-center justify-center gap-2 rounded-md",
        "border border-border bg-surface text-sm font-medium text-text-muted",
        "transition-colors duration-base ease-base",
        "hover:border-border-strong hover:bg-surface-muted hover:text-text",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60",
        "disabled:pointer-events-none disabled:opacity-50",
        iconOnly ? "w-9 shrink-0" : "w-full px-3",
        className,
      )}
    >
      <svg
        aria-hidden="true"
        focusable="false"
        className="h-5 w-5 shrink-0"
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
      {!iconOnly && <span>New chat</span>}
    </button>
  );
}
