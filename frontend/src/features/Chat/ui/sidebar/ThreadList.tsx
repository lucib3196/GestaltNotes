import type { Thread } from "../../../../services";
import ThreadItem from "./ThreadItem";

export type ThreadListProps = {
  threads: Thread[];
  loading: boolean;
  error: string | null;
  selectedThreadId: string | null;
  onSelect: (id: string) => void;
  onRenamed: (thread: Thread) => void;
  onDeleted: (id: string) => void;
  onRetry: () => void;
};

export default function ThreadList({
  threads,
  loading,
  error,
  selectedThreadId,
  onSelect,
  onRenamed,
  onDeleted,
  onRetry,
}: ThreadListProps) {
  return (
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
        <div className="space-y-2 px-3 py-6">
          <p role="alert" className="text-sm text-red-500">
            Failed to load chats
          </p>
          <button
            type="button"
            onClick={onRetry}
            className="rounded-md px-3 py-2 text-sm text-text hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
          >
            Retry
          </button>
        </div>
      ) : threads.length === 0 ? (
        <p className="px-3 py-6 text-center text-sm text-text-soft">
          No chats yet
        </p>
      ) : (
        threads.map((thread) => (
          <ThreadItem
            key={thread.id}
            thread={thread}
            selected={thread.id === selectedThreadId}
            onSelect={onSelect}
            onRenamed={onRenamed}
            onDeleted={onDeleted}
          />
        ))
      )}
    </nav>
  );
}
