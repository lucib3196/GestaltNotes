import MarkdownRenderer from "../../../components/Markdown/MarkdownRenderer";

interface Props {
  title: string;
  message: string;
  version: string;
}

export default function AnnouncementPreview({
  title,
  message,
  version,
}: Props) {
  return (
    <section
      aria-label="Announcement preview"
      className="min-w-0 rounded-2xl border border-border bg-bg p-6"
    >
      <p className="text-xs font-semibold uppercase tracking-widest text-text-soft">
        User preview
      </p>
      <div className="mt-7 flex items-center gap-2">
        <span className="rounded-full bg-accent/10 px-3 py-1 text-xs font-medium text-accent">
          Product update
        </span>
        {version.trim() && (
          <span className="font-mono text-xs text-text-soft">
            v{version.trim()}
          </span>
        )}
      </div>
      <h3 className="mt-5 break-words text-2xl font-semibold leading-tight">
        {title.trim() || "Your announcement title"}
      </h3>
      <div className="mt-4 min-w-0 break-words text-sm leading-7">
        <MarkdownRenderer>
          {message.trim() || "Your message will appear here as you write."}
        </MarkdownRenderer>
      </div>
    </section>
  );
}
