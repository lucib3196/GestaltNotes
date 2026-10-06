import type { CourseNote } from "../../../services/courses";
import { getNoteFormat } from "../utils";

export function CourseNoteBox({
  note,
  selected,
  onSelect,
}: {
  note: CourseNote;
  selected: boolean;
  onSelect: (note: CourseNote) => void;
}) {
  const format = getNoteFormat(note);
  const resourceLabel =
    note.resource_type === "lecture"
      ? "Lecture notes"
      : note.resource_type.charAt(0).toUpperCase() +
        note.resource_type.slice(1);

  return (
    <button
      type="button"
      onClick={() => onSelect(note)}
      aria-pressed={selected}
      className={`flex w-full items-center gap-4 px-4 py-3 text-left transition-colors hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent focus-visible:-outline-offset-2 ${selected ? "bg-surface-muted ring-1 ring-inset ring-accent" : ""}`}
    >
      <span className="min-w-0 flex-1">
        <span
          title={note.title}
          className="block truncate font-semibold text-text"
        >
          {note.title}
        </span>
        <span className="block text-sm text-text-muted">
          {format} · {resourceLabel}
        </span>
      </span>
    </button>
  );
}
