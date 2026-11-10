import {
  Dialog,
  DialogPanel,
  DialogTitle,
  Description,
} from "@headlessui/react";
import { FiBell, FiX } from "react-icons/fi";
import MarkdownRenderer from "../../../components/Markdown/MarkdownRenderer";
import type { Announcement } from "../../../services/announcements";
import { useMarkAnnouncementRead } from "../hooks/useMarkAnnouncementRead";
import { formatDate } from "../utils";

interface Props {
  announcement: Announcement;
  onRead: (id: string) => void;
}

export default function UserAnnouncementDialog({
  announcement,
  onRead,
}: Props) {
  const { markRead, pending, error } = useMarkAnnouncementRead();

  async function close() {
    if (pending) return;
    try {
      await markRead(announcement.id);
      onRead(announcement.id);
    } catch {
      // Keep the message open so saving its read status can be retried.
    }
  }

  return (
    <Dialog open onClose={() => void close()} className="relative z-50">
      <div
        className="fixed inset-0 bg-black/65 backdrop-blur-sm"
        aria-hidden="true"
      />
      <div className="fixed inset-0 overflow-y-auto p-3 sm:p-8">
        <div className="flex min-h-full items-center justify-center">
          <DialogPanel className="w-full max-w-2xl rounded-2xl border border-border bg-surface-strong p-5 shadow-soft sm:p-8">
            <div className="flex items-start justify-between gap-4">
              <div className="rounded-xl bg-accent/10 p-3 text-accent">
                <FiBell size={22} aria-hidden="true" />
              </div>
              <button
                type="button"
                onClick={() => void close()}
                disabled={pending}
                aria-label="Close announcement and mark as read"
                className="rounded-lg p-2 text-text-muted hover:bg-surface-muted focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50"
              >
                <FiX size={22} aria-hidden="true" />
              </button>
            </div>
            <div className="mt-6 flex flex-wrap items-center gap-3 text-xs text-text-soft">
              <span className="rounded-full bg-accent/10 px-3 py-1 font-medium text-accent">
                Product update
              </span>
              <span className="font-mono">v{announcement.version}</span>
              <span>{formatDate(announcement.published_at)}</span>
            </div>
            <DialogTitle className="mt-4 break-words text-2xl font-semibold leading-tight sm:text-3xl">
              {announcement.title}
            </DialogTitle>
            <Description className="mt-3 text-xs leading-5 text-text-soft">
              This announcement will be marked as read when you close it.
            </Description>
            <div className="mt-6 min-w-0 overflow-x-auto break-words text-sm leading-7">
              <MarkdownRenderer>{announcement.message}</MarkdownRenderer>
            </div>
            {error && (
              <div
                role="alert"
                className="mt-6 rounded-xl border border-red-400/30 bg-red-400/10 p-4 text-sm"
              >
                <p className="font-medium text-red-300">
                  We couldn’t save your read status.
                </p>
                <p className="mt-1 text-text-muted">
                  {error.message} Close again to retry.
                </p>
              </div>
            )}
            <div className="mt-7 flex justify-end border-t border-border pt-5">
              <button
                type="button"
                onClick={() => void close()}
                disabled={pending}
                className="rounded-xl bg-accent px-5 py-2.5 text-sm font-semibold text-bg hover:bg-accent-strong focus-visible:ring-2 focus-visible:ring-accent disabled:cursor-wait disabled:opacity-50"
              >
                {pending
                  ? "Saving read status…"
                  : error
                    ? "Retry & close"
                    : "Close & mark as read"}
              </button>
            </div>
          </DialogPanel>
        </div>
      </div>
    </Dialog>
  );
}
