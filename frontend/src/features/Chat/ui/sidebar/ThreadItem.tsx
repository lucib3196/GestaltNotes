import clsx from "clsx";
import type { Thread } from "../../../../services";

export default function ThreadItem({
  thread,
  selected,
  onSelect,
}: {
  thread: Thread;
  selected: boolean;
  onSelect: (id: string) => void;
}) {
  const title = thread.title?.trim() || "New Chat";

  return (
    <button
      type="button"
      onClick={() => onSelect(thread.id)}
      aria-current={selected ? "true" : undefined}
      title={title}
      className={clsx(
        "block w-full rounded-lg border px-3 py-2.5 text-left text-sm",
        "transition-colors focus-visible:outline-none",
        "focus-visible:ring-2 focus-visible:ring-accent/60",
        selected
          ? "border-border bg-surface text-text shadow-sm"
          : "border-transparent text-text-soft hover:bg-surface-muted hover:text-text",
      )}
    >
      <span className="block truncate">{title}</span>
    </button>
  );
}
