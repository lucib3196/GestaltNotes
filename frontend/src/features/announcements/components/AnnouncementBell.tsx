import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../Auth";
import { ANNOUNCEMENT_READ_EVENT, type AnnouncementReadEvent } from "../events";
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/react";
import {
  FiArrowRight,
  FiBell,
  FiCheckCircle,
  FiRefreshCw,
} from "react-icons/fi";
import type { Announcement } from "../../../services/announcements";
import { useUnreadAnnouncements } from "../hooks/useUserAnnouncements";
import { formatDate } from "../utils";
import UserAnnouncementDialog from "./UserAnnouncementDialog";

export default function AnnouncementBell() {
  const { announcements, loading, error, refetch } = useUnreadAnnouncements();
  const [selected, setSelected] = useState<Announcement | null>(null);
  const [acknowledged, setAcknowledged] = useState<Set<string>>(
    () => new Set(),
  );
  const unread = announcements.filter((item) => !acknowledged.has(item.id));

  const { user } = useAuth();
  useEffect(() => {
    function onRead(event: Event) {
      const { announcementId, uid } = (event as AnnouncementReadEvent).detail;
      if (uid !== user?.uid) return;
      // Remove after server confirmation, even if refreshing subsequently fails.
      setAcknowledged((previous) => new Set(previous).add(announcementId));
      void refetch();
    }
    window.addEventListener(ANNOUNCEMENT_READ_EVENT, onRead);
    return () => window.removeEventListener(ANNOUNCEMENT_READ_EVENT, onRead);
  }, [user?.uid, refetch]);

  function read() {
    setSelected(null);
  }

  return (
    <>
      <Popover className="relative">
        {({ close }) => (
          <>
            <PopoverButton
              aria-label={`Announcements${unread.length ? `, ${unread.length} unread` : ""}`}
              onClick={() => void refetch()}
              className="relative inline-flex h-9 w-9 items-center justify-center rounded-full text-text-muted transition hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50 data-open:bg-surface-muted data-open:text-accent"
            >
              <FiBell size={19} aria-hidden="true" />
              {unread.length > 0 && (
                <span
                  aria-hidden="true"
                  className="absolute -right-1 -top-0.5 flex min-h-4 min-w-4 items-center justify-center rounded-full bg-accent px-1 text-[10px] font-bold leading-4 text-bg"
                >
                  {unread.length > 99 ? "99+" : unread.length}
                </span>
              )}
            </PopoverButton>
            <PopoverPanel
              anchor="bottom end"
              portal
              role="region"
              aria-label="Unread announcements"
              className="z-50 mt-3 w-[min(24rem,calc(100vw-1.5rem))] overflow-hidden rounded-2xl border border-border bg-surface-strong shadow-soft outline-none [--anchor-padding:0.75rem]"
            >
              <header className="flex items-center justify-between gap-3 border-b border-border px-5 py-4">
                <div>
                  <h2 className="font-semibold">Announcements</h2>
                  <p className="mt-1 text-xs text-text-soft">
                    Updates for you
                    {unread.length ? ` · ${unread.length} unread` : ""}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => void refetch()}
                  disabled={loading}
                  aria-label="Refresh announcements"
                  className="rounded-lg p-2 text-text-muted hover:bg-surface-muted focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50"
                >
                  <FiRefreshCw
                    className={loading ? "animate-spin" : ""}
                    aria-hidden="true"
                  />
                </button>
              </header>
              <div className="max-h-[min(28rem,65dvh)] overflow-y-auto p-2">
                {loading && unread.length === 0 && (
                  <p
                    role="status"
                    className="px-4 py-8 text-center text-sm text-text-muted"
                  >
                    Checking for updates…
                  </p>
                )}
                {error && (
                  <div
                    role="alert"
                    className="m-2 rounded-xl border border-red-400/30 p-4 text-sm"
                  >
                    <p className="font-medium">
                      Couldn’t refresh announcements.
                    </p>
                    <p className="mt-1 text-text-muted">{error.message}</p>
                    <button
                      type="button"
                      onClick={() => void refetch()}
                      disabled={loading}
                      className="mt-3 text-accent underline disabled:opacity-50"
                    >
                      Try again
                    </button>
                  </div>
                )}
                {!loading && !error && unread.length === 0 && (
                  <div className="px-5 py-10 text-center">
                    <FiCheckCircle
                      size={27}
                      className="mx-auto text-accent"
                      aria-hidden="true"
                    />
                    <h3 className="mt-4 font-semibold">You’re all caught up</h3>
                    <p className="mt-2 text-sm leading-6 text-text-muted">
                      New announcements will appear here.
                    </p>
                  </div>
                )}
                {unread.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => {
                      setSelected(item);
                      close();
                    }}
                    className="group flex w-full gap-3 rounded-xl p-4 text-left transition hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
                  >
                    <span
                      className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-accent"
                      aria-hidden="true"
                    />
                    <span className="min-w-0 flex-1">
                      <span className="block break-words text-sm font-semibold leading-6">
                        {item.title}
                      </span>
                      <span className="mt-2 flex flex-wrap items-center gap-2 text-xs text-text-soft">
                        <span className="font-mono">v{item.version}</span>
                        <span aria-hidden="true">·</span>
                        <span>{formatDate(item.published_at)}</span>
                      </span>
                    </span>
                    <FiArrowRight
                      aria-hidden="true"
                      className="mt-1 shrink-0 text-text-soft transition group-hover:translate-x-1 group-hover:text-accent"
                    />
                  </button>
                ))}
              </div>
              <footer className="border-t border-border p-2">
                <Link
                  to="/annoucements"
                  onClick={() => close()}
                  className="flex items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-semibold text-accent hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
                >
                  View all announcements <FiArrowRight aria-hidden="true" />
                </Link>
              </footer>
            </PopoverPanel>
          </>
        )}
      </Popover>
      {selected && (
        <UserAnnouncementDialog
          key={selected.id}
          announcement={selected}
          onRead={read}
        />
      )}
    </>
  );
}
