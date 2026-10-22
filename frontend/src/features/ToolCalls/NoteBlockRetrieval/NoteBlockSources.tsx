import { useId, useState } from "react";
import {
  FiChevronDown,
  FiExternalLink,
  FiFileText,
  FiMaximize2,
  FiMinimize2,
} from "react-icons/fi";

import { PDFViewer } from "../../../components/Viewer/PDFViewer";
import { useStorageFiles } from "../../../hooks/useLoadFile";
import { useSources } from "./hooks";
import type { NoteBlockDocuments } from "./schema";

type Source = NonNullable<ReturnType<typeof useSources>>[number];

const actionClass =
  "inline-flex min-h-9 items-center justify-center gap-2 rounded-md px-3 " +
  "text-xs font-medium text-text-muted transition-colors " +
  "hover:bg-surface-muted hover:text-text " +
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60";

export function NoteBlockSources({ data }: { data: NoteBlockDocuments }) {
  const sources = useSources(data) ?? [];
  const paths = sources.map((source) => source.path);
  const { files, loading, error, errorsByPath, retry } = useStorageFiles(paths);
  const [selectedPath, setSelectedPath] = useState<string | null>(null);
  const previewId = useId();

  const filesByPath = new Map(files.map((file) => [file.path, file]));
  const selectedFile = files.find((file) => file.path === selectedPath);
  const selectedSource = sources.find(
    (source) => source.path === selectedFile?.path,
  );

  return (
    <section
      aria-label="Lecture sources"
      aria-busy={loading}
      className="w-full min-w-0 overflow-hidden rounded-lg border border-border bg-surface text-text"
    >
      <SourcesHeader count={sources.length} />

      <div className="space-y-2 p-3">
        {loading && (
          <p role="status" className="px-1 py-2 text-sm text-text-muted">
            Loading source PDFs…
          </p>
        )}

        {sources.length === 0 && (
          <p className="px-1 py-2 text-sm text-text-muted">
            No source files available.
          </p>
        )}

        {error && (
          <div
            role="alert"
            className="flex flex-wrap items-center justify-between gap-2 rounded-md bg-surface-muted px-3 py-2"
          >
            <p className="text-xs text-text-muted">{error}</p>
            <button type="button" onClick={retry} className={actionClass}>
              Retry
            </button>
          </div>
        )}

        {sources.map((source) => (
          <SourceRow
            key={source.path}
            source={source}
            available={filesByPath.has(source.path)}
            selected={selectedFile?.path === source.path}
            error={errorsByPath[source.path]}
            previewId={previewId}
            onSelect={() =>
              setSelectedPath((prev) =>
                prev === source.path ? null : source.path,
              )
            }
          />
        ))}
      </div>

      {selectedFile && selectedSource && (
        <SourcePreview
          key={selectedFile.url}
          id={previewId}
          title={selectedSource.title}
          url={selectedFile.url}
        />
      )}
    </section>
  );
}

function SourcesHeader({ count }: { count: number }) {
  return (
    <header className="flex items-center justify-between gap-3 border-b border-border px-4 py-3">
      <div className="flex items-center gap-2">
        <FiFileText aria-hidden="true" className="h-4 w-4 text-accent" />
        <h3 className="text-sm font-semibold">Lecture sources</h3>
      </div>
      <span className="text-xs text-text-soft">
        {count} {count === 1 ? "file" : "files"}
      </span>
    </header>
  );
}

type SourceRowProps = {
  source: Source;
  available: boolean;
  selected: boolean;
  error?: string;
  previewId: string;
  onSelect: () => void;
};

function SourceRow({
  source,
  available,
  selected,
  error,
  previewId,
  onSelect,
}: SourceRowProps) {
  const status = error
    ? "Unavailable"
    : !available
      ? "Loading…"
      : selected
        ? "Viewing"
        : "View PDF";

  return (
    <button
      type="button"
      disabled={!available}
      aria-expanded={selected}
      aria-controls={selected ? previewId : undefined}
      onClick={onSelect}
      className={`flex w-full items-center gap-3 rounded-md border px-3 py-3 text-left transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 disabled:cursor-not-allowed disabled:opacity-60 ${
        selected
          ? "border-accent/40 bg-accent/10"
          : "border-border bg-surface-strong enabled:hover:border-border-strong enabled:hover:bg-surface-muted"
      }`}
    >
      <FiFileText aria-hidden="true" className="h-5 w-5 shrink-0 text-accent" />
      <span className="min-w-0 flex-1">
        <span className="block wrap-break-word text-sm font-medium">
          {source.title}
        </span>
        <span className="mt-1 block text-xs text-text-soft">
          {source.count} matching {source.count === 1 ? "excerpt" : "excerpts"}
        </span>
      </span>
      <span className="shrink-0 text-xs text-text-muted">{status}</span>
      <FiChevronDown
        aria-hidden="true"
        className={`h-4 w-4 shrink-0 transition-transform ${
          selected ? "rotate-180" : ""
        }`}
      />
    </button>
  );
}

function SourcePreview({
  id,
  title,
  url,
}: {
  id: string;
  title: string;
  url: string;
}) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div id={id} className="border-t border-border">
      <div className="flex flex-wrap items-center justify-between gap-2 bg-surface-muted px-3 py-2">
        <p className="min-w-0 flex-1 wrap-break-word text-sm font-medium">
          {title}
        </p>
        <div className="flex flex-wrap items-center gap-1">
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className={actionClass}
          >
            <FiExternalLink aria-hidden="true" />
            Open PDF
          </a>
          <button
            type="button"
            aria-pressed={expanded}
            onClick={() => setExpanded((value) => !value)}
            className={actionClass}
          >
            {expanded ? (
              <FiMinimize2 aria-hidden="true" />
            ) : (
              <FiMaximize2 aria-hidden="true" />
            )}
            {expanded ? "Reduce" : "Expand"}
          </button>
        </div>
      </div>

      <PDFViewer
        src={url}
        title={`${title} PDF`}
        className={
          expanded ? "h-[80vh] min-h-80" : "h-[55vh] min-h-72 max-h-160"
        }
      />
    </div>
  );
}
