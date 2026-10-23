import type { CourseNote } from "../../../services/courses";

type CourseNoteFileProps = {
  note: CourseNote;
  onView?: (note: CourseNote) => void;
};

export default function CourseNoteFile({ note, onView }: CourseNoteFileProps) {
  return (
    <article className="rounded-lg border border-border bg-surface-muted p-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <p className="truncate font-semibold text-text">{note.title}</p>
          <p className="mt-1 text-sm text-text-muted">{note.resource_type}</p>
        </div>

        <button
          type="button"
          onClick={() => onView?.(note)}
          className="w-fit rounded-lg border border-border bg-surface px-3 py-1.5 text-sm font-semibold text-text transition-colors hover:bg-surface-muted"
        >
          View file
        </button>
      </div>
    </article>
  );
}
