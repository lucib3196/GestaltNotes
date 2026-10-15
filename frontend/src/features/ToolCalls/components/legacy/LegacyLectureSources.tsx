import { useEffect, useId, useMemo, useRef, useState } from "react";
import {
  FiChevronDown,
  FiExternalLink,
  FiFileText,
  FiMaximize2,
  FiMinimize2,
  FiX,
} from "react-icons/fi";
import { PDFViewer } from "../../../../components/Viewer/PDFViewer";
import { useLoadFile } from "../../../../hooks/useLoadFile";
import type { LegacySourceDocumentSet } from "../../schemas/legacySources";

export default function LegacyLectureSources({
  data,
}: {
  data: LegacySourceDocumentSet;
}) {
  const sources = useMemo(() => {
    const byPath = new Map<
      string,
      { path: string; title: string; course?: string; count: number }
    >();
    for (const document of data) {
      const path = document.metadata.source_pdf?.trim();
      if (!path) continue;
      const existing = byPath.get(path);
      if (existing) {
        existing.count += 1;
        if (
          existing.title === "Untitled lecture" &&
          document.metadata.lecture_title?.trim()
        ) {
          existing.title = document.metadata.lecture_title.trim();
        }
      } else {
        byPath.set(path, {
          path,
          title: document.metadata.lecture_title?.trim() || "Untitled lecture",
          course: document.metadata.course,
          count: 1,
        });
      }
    }
    return [...byPath.values()];
  }, [data]);
  const paths = useMemo(() => sources.map((source) => source.path), [sources]);
  const { files, loading, error, errorsByPath, retry } = useLoadFile(paths);
  const filesByPath = useMemo(
    () => new Map(files.map((file) => [file.path, file])),
    [files],
  );
  const [selectedPath, setSelectedPath] = useState<string | null>(null);
  const [expanded, setExpanded] = useState(false);
  const previewId = useId();
  const previewRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!selectedPath) return;
    previewRef.current?.scrollIntoView({
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
        ? "auto"
        : "smooth",
      block: "start",
    });
  }, [selectedPath]);
  const selectedSource = sources.find((source) => source.path === selectedPath);
  const selectedFile = selectedSource
    ? filesByPath.get(selectedSource.path)
    : undefined;
  const actionStyle =
    "inline-flex min-h-9 items-center justify-center gap-2 rounded-md px-3 text-xs font-medium text-text-muted transition-colors hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60";

  return (
    <section
      aria-label="Lecture sources"
      aria-busy={loading}
      className="w-full min-w-0 overflow-hidden rounded-lg border border-border bg-surface text-text"
    >
      <div className="flex items-center justify-between gap-3 border-b border-border px-4 py-3">
        <div className="flex items-center gap-2">
          <FiFileText aria-hidden="true" className="h-4 w-4 text-accent" />
          <h3 className="text-sm font-semibold">Lecture sources</h3>
        </div>
        <span className="text-xs text-text-soft">
          {sources.length} {sources.length === 1 ? "PDF" : "PDFs"}
        </span>
      </div>
      <div className="space-y-2 p-3">
        {loading && (
          <p role="status" className="px-1 text-xs text-text-soft">
            Loading source PDFs…
          </p>
        )}
        {sources.length === 0 && (
          <p className="px-1 py-2 text-sm text-text-muted">
            No PDF sources were provided.
          </p>
        )}
        {error && (
          <div
            role="alert"
            className="flex flex-wrap items-center justify-between gap-2 rounded-md bg-surface-muted px-3 py-2"
          >
            <p className="text-xs text-text-muted">{error}</p>
            <button type="button" onClick={retry} className={actionStyle}>
              Retry PDFs
            </button>
          </div>
        )}
        {sources.map((source) => {
          const file = filesByPath.get(source.path);
          const selected = Boolean(
            selectedFile && selectedPath === source.path,
          );
          return (
            <button
              key={source.path}
              type="button"
              disabled={!file}
              aria-expanded={selected}
              aria-controls={selected ? previewId : undefined}
              onClick={() => {
                setSelectedPath(selected ? null : source.path);
                setExpanded(false);
              }}
              className={`flex w-full items-center gap-3 rounded-md border px-3 py-3 text-left transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 disabled:cursor-not-allowed disabled:opacity-60 ${selected ? "border-accent/40 bg-accent/10" : "border-border bg-surface-strong enabled:hover:border-border-strong enabled:hover:bg-surface-muted"}`}
            >
              <FiFileText
                aria-hidden="true"
                className="h-5 w-5 shrink-0 text-accent"
              />
              <span className="min-w-0 flex-1">
                <span className="block break-words text-sm font-medium">
                  {source.title}
                </span>
                <span className="mt-1 block text-xs text-text-soft">
                  {source.course ? `${source.course} · ` : ""}
                  {source.count} matching{" "}
                  {source.count === 1 ? "excerpt" : "excerpts"}
                </span>
              </span>
              <span className="shrink-0 text-xs text-text-muted">
                {errorsByPath[source.path]
                  ? "Unavailable"
                  : !file
                    ? "Loading…"
                    : selected
                      ? "Hide PDF"
                      : "View PDF"}
              </span>
              <FiChevronDown
                aria-hidden="true"
                className={`h-4 w-4 shrink-0 transition-transform ${selected ? "rotate-180" : ""}`}
              />
            </button>
          );
        })}
      </div>
      {selectedSource && selectedFile && (
        <div
          ref={previewRef}
          id={previewId}
          className="scroll-mt-4 border-t border-border"
        >
          <div className="flex flex-wrap items-center justify-between gap-2 bg-surface-muted px-3 py-2">
            <p className="min-w-0 flex-1 wrap-break-word text-sm font-medium">
              {selectedSource.title}
            </p>
            <div className="flex flex-wrap items-center gap-1">
              <a
                href={selectedFile.url}
                target="_blank"
                rel="noopener noreferrer"
                className={actionStyle}
              >
                <FiExternalLink aria-hidden="true" />
                Open in new tab
              </a>
              <button
                type="button"
                onClick={() => setExpanded((value) => !value)}
                aria-pressed={expanded}
                className={actionStyle}
              >
                {expanded ? (
                  <FiMinimize2 aria-hidden="true" />
                ) : (
                  <FiMaximize2 aria-hidden="true" />
                )}
                {expanded ? "Reduce" : "Expand"}
              </button>
              <button
                type="button"
                onClick={() => {
                  setSelectedPath(null);
                  setExpanded(false);
                }}
                aria-label="Close PDF preview"
                className={actionStyle}
              >
                <FiX aria-hidden="true" />
              </button>
            </div>
          </div>
          <PDFViewer
            key={selectedFile.url}
            src={selectedFile.url}
            title={`${selectedSource.title} PDF`}
            className={
              expanded ? "h-[80vh] min-h-80" : "h-[55vh] min-h-72 max-h-[640px]"
            }
          />
          <p className="px-4 py-2 text-xs text-text-soft">
            If the preview is unavailable in your browser, open the PDF in a new
            tab.
          </p>
        </div>
      )}
    </section>
  );
}
