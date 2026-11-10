import { useState } from "react";
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  Description,
} from "@headlessui/react";
import {
  FiCheckCircle,
  FiFileText,
  FiPlus,
  FiRadio,
  FiRefreshCw,
  FiSend,
  FiX,
} from "react-icons/fi";
import type { Announcement } from "../../services/announcements";
import { useAnnouncementActions, useManagedAnnouncements } from "./hooks";
import AnnouncementList from "./components/AnnouncementList";
import AnnouncementDetails from "./components/AnnouncementDetails";
import AnnouncementEditor from "./components/AnnouncementEditor";
import PublishAnnouncementDialog from "./components/PublishAnnouncementDialog";

export default function AnnouncementDashboard() {
  const { announcements, loading, error, refetch } = useManagedAnnouncements();
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<"all" | "draft" | "published">("all");
  const [editor, setEditor] = useState<{
    announcement: Announcement | null;
  } | null>(null);
  const [publishing, setPublishing] = useState<Announcement | null>(null);
  const [deleting, setDeleting] = useState<Announcement | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const actions = useAnnouncementActions();
  const sorted = [...announcements].sort((a, b) =>
    (b.created_at ?? "").localeCompare(a.created_at ?? ""),
  );
  const selected = announcements.find((item) => item.id === selectedId) ?? null;
  const drafts = announcements.filter((item) => !item.published).length;

  function saved(announcement: Announcement) {
    setEditor(null);
    setSelectedId(announcement.id);
    setNotice("Announcement saved.");
    void refetch();
  }
  function published(announcement: Announcement) {
    setPublishing(null);
    setSelectedId(announcement.id);
    setNotice(
      "Announcement published. Your recipients can now read it in the app.",
    );
    void refetch();
  }
  async function remove() {
    if (!deleting) return;
    try {
      await actions.deleteAnnouncement(deleting.id);
      if (selectedId === deleting.id) setSelectedId(null);
      setDeleting(null);
      setNotice("Announcement deleted.");
      void refetch();
    } catch {
      /* Keep the confirmation open and display the error. */
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-2 py-8 sm:px-4 lg:px-6 lg:py-12">
      <header className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">
            Admin workspace
          </p>
          <h1 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">
            Announcements
          </h1>
          <p className="mt-3 max-w-xl text-sm leading-6 text-text-muted">
            Keep your community in the loop. Draft an update, review your
            audience, and share what’s next.
          </p>
        </div>
        <button
          type="button"
          onClick={() => setEditor({ announcement: null })}
          className="inline-flex items-center justify-center gap-2 self-start rounded-xl bg-accent px-5 py-3 text-sm font-semibold text-bg hover:bg-accent-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent sm:self-auto"
        >
          <FiPlus size={18} aria-hidden="true" />
          Create announcement
        </button>
      </header>
      <section
        aria-label="Announcement overview"
        className="mt-8 grid grid-cols-3 gap-3 sm:gap-5"
      >
        {[
          {
            label: "Your announcements",
            value: announcements.length,
            icon: FiRadio,
            hint: "Created by you",
          },
          {
            label: "Drafts",
            value: drafts,
            icon: FiFileText,
            hint: "Ready when you are",
          },
          {
            label: "Published",
            value: announcements.length - drafts,
            icon: FiSend,
            hint: "Shared with recipients",
          },
        ].map(({ label, value, icon: Icon, hint }) => (
          <div
            key={label}
            className="rounded-2xl border border-border bg-surface p-4 sm:p-5"
          >
            <div className="flex items-start justify-between gap-2">
              <p className="text-xs font-medium text-text-muted sm:text-sm">
                {label}
              </p>
              <Icon
                aria-hidden="true"
                className="hidden text-accent/70 sm:block"
              />
            </div>
            <p className="mt-3 text-3xl font-semibold tabular-nums">
              {loading && announcements.length === 0 ? "—" : value}
            </p>
            <p className="mt-2 hidden text-xs text-text-soft sm:block">
              {hint}
            </p>
          </div>
        ))}
      </section>
      {notice && (
        <div
          role="status"
          className="mt-6 flex items-start gap-3 rounded-xl border border-accent/30 bg-accent/10 px-4 py-3 text-sm"
        >
          <FiCheckCircle
            aria-hidden="true"
            className="mt-0.5 shrink-0 text-accent"
          />
          <p className="flex-1">{notice}</p>
          <button
            type="button"
            onClick={() => setNotice(null)}
            aria-label="Dismiss notification"
            className="rounded p-1"
          >
            <FiX />
          </button>
        </div>
      )}
      <div className="mt-9 flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Your workspace</h2>
        <button
          type="button"
          onClick={() => void refetch()}
          disabled={loading}
          className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium text-text-muted hover:bg-surface-muted disabled:opacity-50"
        >
          <FiRefreshCw
            aria-hidden="true"
            className={loading ? "animate-spin" : ""}
          />
          Refresh
        </button>
      </div>
      <p className="mt-1 text-xs text-text-soft">
        Only announcements you own appear here.
      </p>
      {error && (
        <div
          role="alert"
          className="mt-5 rounded-xl border border-red-400/30 bg-red-400/10 p-5"
        >
          <p className="font-medium">Couldn’t refresh your announcements</p>
          <p className="mt-2 text-sm text-text-muted">{error.message}</p>
          <button
            type="button"
            onClick={() => void refetch()}
            disabled={loading}
            className="mt-3 text-sm text-accent underline"
          >
            Try again
          </button>
        </div>
      )}
      {loading && announcements.length === 0 && (
        <div
          role="status"
          className="py-20 text-center text-sm text-text-muted"
        >
          Loading your announcements…
        </div>
      )}
      {!loading && !error && announcements.length === 0 && (
        <section className="mt-6 flex flex-col items-center rounded-2xl border border-dashed border-border bg-surface px-6 py-16 text-center">
          <span className="rounded-2xl bg-accent/10 p-4 text-accent">
            <FiRadio size={30} aria-hidden="true" />
          </span>
          <h2 className="mt-6 text-xl font-semibold">
            Your next update starts here
          </h2>
          <p className="mt-3 max-w-md text-sm leading-6 text-text-muted">
            Share a feature release, a helpful tip, or an important update. Your
            first announcement stays a draft until you publish it.
          </p>
          <button
            type="button"
            onClick={() => setEditor({ announcement: null })}
            className="mt-6 inline-flex items-center gap-2 rounded-xl bg-accent px-5 py-3 text-sm font-semibold text-bg hover:bg-accent-strong"
          >
            <FiPlus aria-hidden="true" />
            Create your first announcement
          </button>
        </section>
      )}
      {announcements.length > 0 && (
        <div className="mt-5 grid items-start gap-6 lg:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)]">
          <AnnouncementList
            announcements={sorted}
            selectedId={selectedId}
            onSelect={setSelectedId}
            search={search}
            onSearch={setSearch}
            filter={filter}
            onFilter={setFilter}
          />
          {selected ? (
            <AnnouncementDetails
              key={`${selected.id}:${selected.updated_at}:${selected.published}`}
              announcement={selected}
              onEdit={() => setEditor({ announcement: selected })}
              onPublish={() => setPublishing(selected)}
              onDelete={() => setDeleting(selected)}
            />
          ) : (
            <aside className="rounded-2xl border border-dashed border-border p-10 text-center">
              <FiFileText
                aria-hidden="true"
                className="mx-auto text-3xl text-text-soft"
              />
              <h2 className="mt-4 font-semibold">A closer look</h2>
              <p className="mt-2 text-sm leading-6 text-text-muted">
                Select an announcement to read it, check its audience, or
                continue editing.
              </p>
            </aside>
          )}
        </div>
      )}
      {editor && (
        <AnnouncementEditor
          key={editor.announcement?.id ?? "new"}
          announcement={editor.announcement}
          onClose={() => setEditor(null)}
          onSaved={saved}
        />
      )}
      {publishing && (
        <PublishAnnouncementDialog
          announcement={publishing}
          onClose={() => setPublishing(null)}
          onPublished={published}
        />
      )}
      {deleting && (
        <Dialog
          open
          onClose={() => {
            if (!actions.pending) setDeleting(null);
          }}
          className="relative z-50"
        >
          <div
            className="fixed inset-0 bg-black/65 backdrop-blur-sm"
            aria-hidden="true"
          />
          <div className="fixed inset-0 flex items-center justify-center p-4">
            <DialogPanel className="w-full max-w-md rounded-2xl border border-border bg-surface-strong p-6 shadow-soft">
              <DialogTitle className="text-xl font-semibold">
                Delete announcement?
              </DialogTitle>
              <Description className="mt-3 break-words text-sm leading-6 text-text-muted">
                “{deleting.title}” and its recipient records will be permanently
                deleted. This cannot be undone.
              </Description>
              {actions.error && (
                <p role="alert" className="mt-4 text-sm text-red-300">
                  {actions.error.message}
                </p>
              )}
              <div className="mt-6 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setDeleting(null)}
                  disabled={actions.pending}
                  className="rounded-xl border border-border px-4 py-2.5 text-sm disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={() => void remove()}
                  disabled={actions.pending}
                  className="rounded-xl bg-red-500 px-4 py-2.5 text-sm font-semibold text-white hover:bg-red-600 disabled:opacity-50"
                >
                  {actions.pending ? "Deleting…" : "Delete announcement"}
                </button>
              </div>
            </DialogPanel>
          </div>
        </Dialog>
      )}
    </div>
  );
}
