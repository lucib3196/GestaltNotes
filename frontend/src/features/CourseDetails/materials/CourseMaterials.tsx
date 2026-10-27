import type { useCourseMaterials } from "../hooks/useCourseMaterials";
import { NoteOverviewBox } from "./NoteOverviewBox";
import { useCourseDetailsStore } from "../state";
import { useEffect } from "react";
type Props = {
  materials: ReturnType<typeof useCourseMaterials>;
};

export default function CourseMaterials({ materials }: Props) {
  const { notes, loading, error, refetch, refreshNote } = materials;
  const setNotes = useCourseDetailsStore((s) => s.setNotes);
  useEffect(() => setNotes(notes), [notes, setNotes]);

  return (
    <section
      aria-label="Course materials"
      aria-busy={loading}
      className="min-w-0 space-y-3"
    >
      <header className="flex items-center justify-between gap-3">
        <h2 className="text-sm font-semibold text-text">Course materials</h2>
        {!loading && !error && (
          <span className="text-sm text-text-muted">
            {notes.length} {notes.length === 1 ? "file" : "files"}
          </span>
        )}
      </header>

      {loading ? (
        <p role="status" className="text-sm text-text-muted">
          Loading materials…
        </p>
      ) : error ? (
        <div role="alert" className="rounded-xl bg-surface-muted p-4">
          <p className="text-sm text-text-muted">{error.message}</p>
          <button
            type="button"
            onClick={() => void refetch().catch(() => {})}
            className="mt-2 rounded text-sm text-accent underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
          >
            Try again
          </button>
        </div>
      ) : notes.length === 0 ? (
        <p className="rounded-xl bg-surface-muted/40 p-6 text-sm text-text-muted">
          No course materials yet.
        </p>
      ) : (
        <ul className="max-h-[65vh] space-y-2 overflow-y-auto overscroll-contain">
          {notes.map((note) => (
            <li key={note.id} className="min-w-0">
              <NoteOverviewBox note={note} onRefresh={refreshNote} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
