import { MdOpenInNew } from "react-icons/md";
import type { WebSearchSources as Sources } from "./schema";

export function WebSearchSources({ data }: { data: Sources }) {
  const sources = Array.from(
    new Map(data.map((source) => [source.url, source])).values(),
  );

  if (sources.length === 0) {
    return (
      <p className="text-xs text-text-soft">
        No source links were returned for this search.
      </p>
    );
  }

  return (
    <section
      aria-label="Web search sources"
      className="min-w-0 w-full bg-inherit px-3 py-3 text-text  sm:px-4"
    >
      <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-text-soft">
        Sources
      </h3>
      <ul className="space-y-1 flex flex-row flex-wrap">
        {sources.map((source) => {
          const hostname = new URL(source.url).hostname;
          const title = source.title?.trim() || hostname;

          return (
            <li key={source.url}>
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`${title} (opens in a new tab)`}
                className="flex min-h-11 items-center gap-3 rounded-lg px-2 py-2 transition-colors hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
              >
                <span className="min-w-0 flex-1">
                  <span className="block wrap-break-word text-sm font-medium">
                    {title}
                  </span>
                  {/* <span className="block break-words text-xs text-text-soft">
                    {hostname}
                  </span> */}
                </span>
                <MdOpenInNew
                  aria-hidden="true"
                  className="h-4 w-4 shrink-0 text-text-muted"
                />
              </a>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
