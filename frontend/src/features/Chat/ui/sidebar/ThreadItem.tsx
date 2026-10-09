import clsx from "clsx";
import { useState } from "react";
import { useDeleteThread } from "../../hooks/useDeleteThread";
import RenameThreadDialog from "./RenameThreadDialog";
import ThreadActionsMenu from "./ThreadActionsMenu";
import type { Thread } from "../../../../services";

export type ThreadItemProps = {
  thread: Thread;
  selected: boolean;
  onSelect: (id: string) => void;
  onRenamed: (thread: Thread) => void;
  onDeleted: (id: string) => void;
};

export default function ThreadItem({
  thread,
  selected,
  onSelect,
  onRenamed,
  onDeleted,
}: ThreadItemProps) {
  const [showModal, setShowModal] = useState<boolean>(false);
  const { deleteThread, loading: deleting } = useDeleteThread();
  const [deleteError, setDeleteError] = useState<string | null>(null);

  async function handleDelete() {
    setDeleteError(null);
    try {
      await deleteThread(thread.id);
      onDeleted(thread.id);
    } catch {
      setDeleteError("Could not delete this chat. Please try again.");
    }
  }

  const displayTitle = thread.title?.trim() || "New Chat";

  return (
    <div
      className={clsx(
        "relative flex min-w-0 flex-wrap items-center gap-1 rounded-lg border p-1",
        "transition-colors duration-base",
        selected
          ? "border-accent/30 bg-accent/10 text-text"
          : "border-transparent text-text-soft hover:border-border hover:bg-surface-muted",
      )}
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

      <ThreadActionsMenu
        title={displayTitle}
        deleting={deleting}
        onRename={() => setShowModal(true)}
        onDelete={() => void handleDelete()}
      />
      {deleteError && (
        <p role="alert" className="w-full px-2 pb-1 text-xs text-red-500">
          {deleteError}
        </p>
      )}
      {showModal && (
        <RenameThreadDialog
          thread={thread}
          onClose={() => setShowModal(false)}
          onRenamed={onRenamed}
        />
      )}
    </div>
  );
}
