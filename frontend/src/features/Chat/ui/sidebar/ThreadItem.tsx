import clsx from "clsx";
import { useState } from "react";
import { HiDotsHorizontal } from "react-icons/hi";
import type { Thread } from "../../../../services";
import Modal
export default function ThreadItem({
  thread,
  selected,
  onSelect,
}: {
  thread: Thread;
  selected: boolean;
  onSelect: (id: string) => void;
}) {
  const [popUp, setPopUp] = useState(false);
  const displayTitle = thread.title?.trim() || "New Chat";

  return (
    <div
      className={clsx(
        "relative flex min-w-0 items-center gap-1 rounded-lg border p-1",
        "transition-colors duration-base",
        selected
          ? "border-accent/30 bg-accent/10 text-text"
          : "border-transparent text-text-soft hover:border-border hover:bg-surface-muted",
      )}
      onKeyDown={(event) => {
        if (event.key === "Escape") setPopUp(false);
      }}
    >
      <button
        type="button"
        onClick={() => onSelect(thread.id)}
        aria-current={selected ? "true" : undefined}
        title={displayTitle}
        className="min-w-0 flex-1 rounded-md px-2 py-2 text-left text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
      >
        <span className={clsx("block truncate", selected && "font-medium")}>
          {displayTitle}
        </span>
      </button>

      <button
        type="button"
        onClick={() => setPopUp((value) => !value)}
        aria-label={`Options for ${displayTitle}`}
        aria-expanded={popUp}
        className={clsx(
          "inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-md",
          "text-text-soft transition-colors hover:bg-surface hover:text-text",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60",
          popUp && "bg-surface text-text",
        )}
      >
        <HiDotsHorizontal aria-hidden="true" className="h-4 w-4" />
      </button>

      {popUp && (
        <div className="absolute right-0 top-full z-20 mt-1 w-44 rounded-lg border border-border bg-surface-strong p-2 text-sm text-text shadow-lg">
          <div className="flex flex-col gap-2 mx-2 my-2">
            <span>Rename</span>
            <span>Delete</span>
          </div>
        </div>
      )}
    </div>
  );
}
