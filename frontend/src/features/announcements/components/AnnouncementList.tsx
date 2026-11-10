import { FiArrowRight, FiSearch } from "react-icons/fi";
import type { Announcement } from "../../../services/announcements";
import { formatDate } from "../utils";

export function StatusBadge({ published }: { published: boolean }) {
  return (
    <span
      className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${published ? "bg-accent-strong/15 text-accent-strong" : "bg-accent/10 text-accent"}`}
    >
      <span aria-hidden="true">{published ? "●" : "○"}&nbsp;</span>
      {published ? "Published" : "Draft"}
    </span>
  );
}

type Filter = "all" | "draft" | "published";
interface Props {
  announcements: Announcement[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  search: string;
  onSearch: (value: string) => void;
  filter: Filter;
  onFilter: (value: Filter) => void;
}

export default function AnnouncementList({
  announcements,
  selectedId,
  onSelect,
  search,
  onSearch,
  filter,
  onFilter,
}: Props) {
  const visible = announcements.filter(
    (item) =>
      (filter === "all" || item.published === (filter === "published")) &&
      `${item.title} ${item.message} ${item.version}`
        .toLowerCase()
        .includes(search.toLowerCase()),
  );
  return (
    <section aria-label="Your announcements" className="min-w-0">
      <div className="flex flex-col gap-4 border-b border-border pb-5 sm:flex-row sm:items-center sm:justify-between">
        <div
          className="flex gap-1 rounded-xl bg-surface-muted p-1"
          aria-label="Filter announcements"
        >
          {(["all", "draft", "published"] as const).map((value) => (
            <button
              key={value}
              type="button"
              aria-pressed={filter === value}
              onClick={() => onFilter(value)}
              className={`rounded-lg px-3 py-2 text-sm font-medium transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ${filter === value ? "bg-surface-strong text-text shadow-sm" : "text-text-muted hover:text-text"}`}
            >
              {value === "all"
                ? "All announcements"
                : value === "draft"
                  ? "Drafts"
                  : "Published"}
            </button>
          ))}
        </div>
        <label className="flex items-center gap-2 rounded-xl border border-border bg-surface px-3 py-2.5 sm:max-w-56">
          <FiSearch className="shrink-0 text-text-soft" aria-hidden="true" />
          <span className="sr-only">Search announcements</span>
          <input
            type="search"
            value={search}
            onChange={(event) => onSearch(event.target.value)}
            placeholder="Search announcements"
            className="min-w-0 w-full bg-transparent text-sm outline-none placeholder:text-text-soft"
          />
        </label>
      </div>
      <div className="mt-4 space-y-3">
        {visible.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => onSelect(item.id)}
            aria-pressed={selectedId === item.id}
            className={`group w-full rounded-2xl border p-5 text-left transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ${selectedId === item.id ? "border-accent/70 bg-accent/5" : "border-border bg-surface hover:border-border-strong hover:bg-surface-strong"}`}
          >
            <div className="flex items-center justify-between gap-3">
              <StatusBadge published={item.published} />
              <span className="font-mono text-xs text-text-soft">
                v{item.version}
              </span>
            </div>
            <div className="mt-4 flex items-start justify-between gap-4">
              <h2 className="break-words text-lg font-semibold tracking-tight">
                {item.title}
              </h2>
              <FiArrowRight
                aria-hidden="true"
                className="mt-1 shrink-0 text-text-soft transition group-hover:translate-x-1 group-hover:text-accent"
              />
            </div>
            <p className="mt-2 line-clamp-2 break-words text-sm leading-6 text-text-muted">
              {item.message}
            </p>
            <div className="mt-5 flex flex-wrap items-center justify-between gap-2 text-xs text-text-soft">
              <span>{item.audience_summary || "Audience not selected"}</span>
              <span>
                {item.published ? "Published" : "Created"}{" "}
                {formatDate(
                  item.published ? item.published_at : item.created_at,
                )}
              </span>
            </div>
          </button>
        ))}
        {visible.length === 0 && (
          <div className="rounded-2xl border border-dashed border-border px-6 py-14 text-center">
            <h2 className="font-semibold">No matching announcements</h2>
            <p className="mt-2 text-sm text-text-muted">
              Try another search or filter.
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
