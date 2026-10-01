import type { CourseNote } from "../../../services/courses";

type Props = {
  note: CourseNote;
};

export function CourseNoteView({ note }: Props) {
  return (
    <article className="rounded-lg border border-border bg-surface-muted p-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <p className="truncate font-semibold text-text">{note.title}</p>
          <p className="mt-1 text-sm text-text-muted">{note.resource_type}</p>
        </div>
      </div>
    </article>
  );
}
