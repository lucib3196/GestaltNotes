import { useId, useState } from "react";
import NoteBlockRenderer from "./components/NoteBlockRenderer";
import type { NoteBlockKind } from "./schemas";
import { useNoteBlocks } from "./useNoteBlocks";

const filters: { value: "all" | NoteBlockKind; label: string }[] = [
  { value: "all", label: "All" },
  { value: "lecture_summary", label: "Lecture summaries" },
  { value: "extracted_question", label: "Extracted questions" },
  { value: "derivation", label: "Derivations" },
  { value: "conceptual_question", label: "Conceptual questions" },
];

export type NoteBlocksProps = { courseId: string; fileId: string };

export default function NoteBlocks({ courseId, fileId }: NoteBlocksProps) {
  const { blocks, loading, error } = useNoteBlocks(courseId, fileId);
  const [selectedKind, setSelectedKind] = useState<"all" | NoteBlockKind>("all");
  const [page, setPage] = useState(0);
  const selectId = useId();
  const visibleBlocks = blocks
    .filter((block) => selectedKind === "all" || block.kind === selectedKind)
    .sort((a, b) => a.position - b.position || a.id.localeCompare(b.id));

  const currentPage = Math.min(page, Math.max(visibleBlocks.length - 1, 0));
  const currentBlock = visibleBlocks[currentPage];

  return (
    <section aria-label="Processed note blocks" className="min-w-0 space-y-4 text-text">
      <div className="flex flex-wrap items-center gap-3">
        <label htmlFor={selectId} className="text-sm font-medium">Content type</label>
        <select
          id={selectId}
          value={selectedKind}
          onChange={(event) => {
            const filter = filters.find((entry) => entry.value === event.target.value);
            if (filter) {
              setSelectedKind(filter.value);
              setPage(0);
            }
          }}
          className="rounded-md border border-border bg-surface px-3 py-2 text-sm text-text focus-visible:outline-2 focus-visible:outline-accent"
        >
          {filters.map((filter) => (
            <option key={filter.value} value={filter.value}>{filter.label}</option>
          ))}
        </select>
      </div>
      {loading ? <p role="status">Loading note blocks…</p>
        : error ? <p role="alert">{error}</p>
        : blocks.length === 0 ? <p>No processed blocks are available for this file.</p>
        : visibleBlocks.length === 0 ? <p>No blocks match this content type.</p>
        : currentBlock && (
          <div className="overflow-hidden ">
            <article
              key={currentBlock.id}
              aria-label="Current note block"
              tabIndex={0}
              className="max-h-[60vh] min-w-0 space-y-3 overflow-y-auto overscroll-contain p-4 focus-visible:outline-2 focus-visible:outline-accent sm:p-5"
            >
              <p className="text-xs font-semibold uppercase tracking-wide text-accent">
                {filters.find((filter) => filter.value === currentBlock.kind)?.label
                  ?? currentBlock.kind
                  ?? "Note block"}
              </p>
              <NoteBlockRenderer block={currentBlock} />
            </article>

            <nav
              aria-label="Note block pagination"
              className="flex items-center justify-between gap-3 px-4 py-3"
            >
              <button
                type="button"
                disabled={currentPage === 0}
                onClick={() => setPage(currentPage - 1)}
                className="rounded-md border border-border px-3 py-2 text-sm hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-40"
              >
                Previous
              </button>
              <p role="status" className="text-sm text-text-muted">
                {currentPage + 1} of {visibleBlocks.length}
              </p>
              <button
                type="button"
                disabled={currentPage === visibleBlocks.length - 1}
                onClick={() => setPage(currentPage + 1)}
                className="rounded-md border border-border px-3 py-2 text-sm hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-40"
              >
                Next
              </button>
            </nav>
          </div>
        )}
    </section>
  );
}
