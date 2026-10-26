import { FiFileText } from "react-icons/fi";
import type { CourseNote } from "../../../services/courses";
import { getNoteFormat } from "../utils/getNoteFormat";

export function CourseNoteDetails({ note }: { note: CourseNote }) {
  return (
    <>
      <FiFileText
        aria-hidden="true"
        className="shrink-0 text-accent"
        size={20}
      />
      <span className="min-w-0 flex-1">
        <span
          title={note.title}
          className="block truncate text-sm font-semibold text-text"
        >
          {note.title}
        </span>
        <span className="mt-1 block text-xs uppercase tracking-wide text-text-muted">
          {getNoteFormat(note)}
        </span>
      </span>
    </>
  );
}
