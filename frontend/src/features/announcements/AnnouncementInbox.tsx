import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  FiArrowLeft,
  FiArrowRight,
  FiBell,
  FiCheck,
  FiRefreshCw,
} from "react-icons/fi";
import type { Announcement } from "../../services/announcements";
import { useAuth } from "../Auth";
import UserAnnouncementDialog from "./components/UserAnnouncementDialog";
import { useAnnouncementHistory } from "./hooks/useUserAnnouncements";
import { formatDate } from "./utils";

export default function AnnouncementInbox() {
  const { user } = useAuth();
  return <AnnouncementInboxContent key={user?.uid ?? "guest"} />;
}

function AnnouncementInboxContent() {
  const [searchParams, setSearchParams] = useSearchParams();
  const parsedPage = Number(searchParams.get("page") ?? 1);
  const page =
    Number.isSafeInteger(parsedPage) &&
    parsedPage > 0 &&
    parsedPage <= Math.floor(Number.MAX_SAFE_INTEGER / 5)
      ? parsedPage
      : 1;
  const { data, loading, error, refetch } = useAnnouncementHistory(page);
  const [selected, setSelected] = useState<Announcement | null>(null);
  const totalPages = data ? Math.max(1, Math.ceil(data.total / 5)) : 1;

  useEffect(() => {
    if (!data || page <= totalPages) return;
    setSearchParams(
      (previous) => {
        const next = new URLSearchParams(previous);
        next.set("page", String(totalPages));
        return next;
      },
      { replace: true },
    );
  }, [data, page, totalPages, setSearchParams]);

  function goToPage(nextPage: number) {
    setSearchParams((previous) => {
      const next = new URLSearchParams(previous);
      next.set("page", String(nextPage));
      return next;
    });
  }

  return (
    <div className="mx-auto max-w-4xl px-2 py-8 sm:px-5 sm:py-12">
      <header className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">
            Your inbox
          </p>
          <h1 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">
            Announcements
          </h1>
          <p className="mt-3 max-w-xl text-sm leading-6 text-text-muted">
            Revisit every update shared with you, including announcements you’ve
            already read.
          </p>
        </div>
        <button
          type="button"
          onClick={() => void refetch()}
          disabled={loading}
          className="inline-flex items-center justify-center gap-2 self-start rounded-xl border border-border px-4 py-2.5 text-sm font-medium text-text-muted hover:bg-surface-muted focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50"
        >
          <FiRefreshCw
            aria-hidden="true"
            className={loading ? "animate-spin" : ""}
          />
          Refresh inbox
        </button>
      </header>
      {error && (
        <div
          role="alert"
          className="mt-7 rounded-xl border border-red-400/30 bg-red-400/10 p-5"
        >
          <p className="font-medium">Couldn’t load your announcements.</p>
          <p className="mt-2 text-sm text-text-muted">{error.message}</p>
          <button
            type="button"
            onClick={() => void refetch()}
            disabled={loading}
            className="mt-3 text-sm text-accent underline disabled:opacity-50"
          >
            Try again
          </button>
        </div>
      )}
      {loading && (
        <p role="status" className="py-12 text-center text-sm text-text-muted">
          Loading your announcements…
        </p>
      )}
      {!loading && !error && data?.total === 0 && (
        <section className="mt-8 rounded-2xl border border-dashed border-border bg-surface px-6 py-16 text-center">
          <FiBell
            aria-hidden="true"
            size={30}
            className="mx-auto text-accent"
          />
          <h2 className="mt-5 text-xl font-semibold">No announcements yet</h2>
          <p className="mt-3 text-sm text-text-muted">
            Updates assigned to you will appear here.
          </p>
        </section>
      )}
      {data && data.total > 0 && page <= totalPages && (
        <>
          <div className="mt-8 flex flex-wrap items-center justify-between gap-3 border-b border-border pb-4">
            <h2 className="font-semibold">All your updates</h2>
            <p className="text-xs text-text-soft">
              Showing {data.offset + 1}–
              {Math.min(data.offset + data.items.length, data.total)} of{" "}
              {data.total}
            </p>
          </div>
          <ul
            aria-label="Assigned announcements"
            aria-busy={loading}
            className="mt-4 space-y-3"
          >
            {data.items.map(({ announcement, read_at }) => (
              <li key={announcement.id}>
                <button
                  type="button"
                  onClick={() => setSelected(announcement)}
                  className="group flex w-full items-start gap-4 rounded-2xl border border-border bg-surface p-5 text-left transition hover:border-border-strong hover:bg-surface-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent sm:p-6"
                >
                  <span
                    className={`mt-0.5 rounded-xl p-2.5 ${read_at ? "bg-surface-muted text-text-soft" : "bg-accent/10 text-accent"}`}
                  >
                    {read_at ? (
                      <FiCheck aria-hidden="true" size={18} />
                    ) : (
                      <FiBell aria-hidden="true" size={18} />
                    )}
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="flex flex-wrap items-center gap-3">
                      <span
                        className={`rounded-full px-2.5 py-1 text-xs font-semibold ${read_at ? "bg-surface-muted text-text-soft" : "bg-accent/10 text-accent"}`}
                      >
                        {read_at ? "Read" : "Unread"}
                      </span>
                      <span className="font-mono text-xs text-text-soft">
                        v{announcement.version}
                      </span>
                    </span>
                    <span className="mt-3 block break-words text-lg font-semibold leading-7">
                      {announcement.title}
                    </span>
                    <span className="mt-2 block text-xs text-text-soft">
                      Published {formatDate(announcement.published_at)}
                      {read_at ? ` · Read ${formatDate(read_at)}` : ""}
                    </span>
                  </span>
                  <FiArrowRight
                    aria-hidden="true"
                    className="mt-2 shrink-0 text-text-soft transition group-hover:translate-x-1 group-hover:text-accent"
                  />
                </button>
              </li>
            ))}
          </ul>
          <nav
            aria-label="Announcement pagination"
            className="mt-7 flex flex-wrap items-center justify-between gap-3 border-t border-border pt-5"
          >
            <button
              type="button"
              onClick={() => goToPage(page - 1)}
              disabled={loading || page <= 1}
              className="inline-flex items-center gap-2 rounded-xl border border-border px-4 py-2.5 text-sm hover:bg-surface-muted focus-visible:ring-2 focus-visible:ring-accent disabled:cursor-not-allowed disabled:opacity-40"
            >
              <FiArrowLeft aria-hidden="true" />
              Previous
            </button>
            <p aria-live="polite" className="text-sm text-text-muted">
              Page {page} of {totalPages}
            </p>
            <button
              type="button"
              onClick={() => goToPage(page + 1)}
              disabled={loading || page >= totalPages}
              className="inline-flex items-center gap-2 rounded-xl border border-border px-4 py-2.5 text-sm hover:bg-surface-muted focus-visible:ring-2 focus-visible:ring-accent disabled:cursor-not-allowed disabled:opacity-40"
            >
              Next
              <FiArrowRight aria-hidden="true" />
            </button>
          </nav>
        </>
      )}
      {selected && (
        <UserAnnouncementDialog
          key={selected.id}
          announcement={selected}
          onRead={() => setSelected(null)}
        />
      )}
    </div>
  );
}
