import MarkdownRenderer from "../../../components/Markdown/MarkdownRenderer";
import { FiEdit2, FiSend, FiTrash2, FiUsers } from "react-icons/fi";
import type { Announcement } from "../../../services/announcements";
import { useAnnouncementAudience } from "../hooks";
import { StatusBadge } from "./AnnouncementList";
import { formatDate } from "../utils";

export default function AnnouncementDetails({
  announcement,
  onEdit,
  onPublish,
  onDelete,
}: {
  announcement: Announcement;
  onEdit: () => void;
  onPublish: () => void;
  onDelete: () => void;
}) {
  const audience = useAnnouncementAudience(announcement.id);
  return (
    <aside
      aria-label="Announcement details"
      className="min-w-0 self-start rounded-2xl border border-border bg-surface p-5 lg:sticky lg:top-16 lg:p-6"
    >
      <div className="flex items-center justify-between gap-3">
        <span className="text-xs font-semibold uppercase tracking-widest text-text-soft">
          Announcement details
        </span>
        <StatusBadge published={announcement.published} />
      </div>
      <h2 className="mt-6 wrap-break-word text-2xl font-semibold leading-tight">
        {announcement.title}
      </h2>
      <p className="mt-3 font-mono text-xs text-text-soft">
        Version {announcement.version}
      </p>
      <div className="mt-5 min-w-0 break-words text-sm leading-7">
        <MarkdownRenderer>{announcement.message}</MarkdownRenderer>
      </div>
      <dl className="mt-6 space-y-3 border-t border-border pt-5 text-xs">
        <div className="flex justify-between gap-3">
          <dt className="text-text-soft">Created</dt>
          <dd>{formatDate(announcement.created_at)}</dd>
        </div>
        <div className="flex justify-between gap-3">
          <dt className="text-text-soft">Last updated</dt>
          <dd>{formatDate(announcement.updated_at)}</dd>
        </div>
        {announcement.published && (
          <div className="flex justify-between gap-3">
            <dt className="text-text-soft">Published</dt>
            <dd>{formatDate(announcement.published_at)}</dd>
          </div>
        )}
      </dl>
      <section
        aria-label="Audience metrics"
        className="mt-6 rounded-xl border border-border bg-bg p-4"
      >
        <h3 className="flex items-center gap-2 text-sm font-semibold">
          <FiUsers className="text-accent" aria-hidden="true" /> Audience
        </h3>
        {audience.loading && (
          <p role="status" className="mt-3 text-sm text-text-muted">
            Loading audience…
          </p>
        )}
        {audience.error && (
          <div role="alert" className="mt-3 text-sm text-text-muted">
            <p>{audience.error.message}</p>
            <button
              type="button"
              onClick={() => void audience.refetch()}
              className="mt-2 text-accent underline"
            >
              Retry
            </button>
          </div>
        )}
        {audience.data && (
          <>
            <dl className="mt-4 grid grid-cols-3 gap-3 text-center">
              {[
                ["Assigned", audience.data.existing_recipients],
                ["Read", audience.data.read_recipients],
                ["Unread", audience.data.unread_recipients],
              ].map(([label, value]) => (
                <div key={label}>
                  <dd className="text-xl font-semibold tabular-nums">
                    {Number(value).toLocaleString()}
                  </dd>
                  <dt className="mt-1 text-xs text-text-soft">{label}</dt>
                </div>
              ))}
            </dl>
            <p className="mt-4 border-t border-border pt-3 text-xs leading-5 text-text-muted">
              {announcement.published
                ? announcement.audience_summary || "Assigned recipients"
                : `${audience.data.total_users.toLocaleString()} current users available for publication.`}
            </p>
          </>
        )}
      </section>
      <div className="mt-6 flex flex-col gap-3">
        {!announcement.published && (
          <button
            type="button"
            onClick={onPublish}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-accent px-4 py-3 text-sm font-semibold text-bg hover:bg-accent-strong focus-visible:ring-2 focus-visible:ring-accent"
          >
            <FiSend aria-hidden="true" />
            Review & publish
          </button>
        )}
        <button
          type="button"
          onClick={onEdit}
          className="inline-flex items-center justify-center gap-2 rounded-xl border border-border px-4 py-2.5 text-sm font-medium hover:bg-surface-muted focus-visible:ring-2 focus-visible:ring-accent"
        >
          <FiEdit2 aria-hidden="true" />
          Edit {announcement.published ? "announcement" : "draft"}
        </button>
        <button
          type="button"
          onClick={onDelete}
          className="inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm text-text-soft hover:bg-red-400/10 hover:text-red-300 focus-visible:ring-2 focus-visible:ring-accent"
        >
          <FiTrash2 aria-hidden="true" />
          Delete announcement
        </button>
      </div>
    </aside>
  );
}
