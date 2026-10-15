import { FiChevronRight, FiFileText } from "react-icons/fi";
import type { CourseContentType, CourseNote } from "../../../services/courses";
import { ContentTypeDropDown } from "../../CourseNote/components/ContentTypeDropDown";
import { getNoteFormat } from "../utils";

type CourseNoteProps = {
  note: CourseNote;
  selected: boolean;
  checked: boolean;
  updating: boolean;
  disabled: boolean;
  onSelect: (note: CourseNote) => void;
  onChecked: (note: CourseNote) => void;
  onTypeChange: (note: CourseNote, type: CourseContentType) => void;
};

export function CourseNoteBox({
  note, selected, checked, updating, disabled, onSelect, onChecked, onTypeChange,
}: CourseNoteProps) {
  return (
    <div className={`rounded-xl p-3 transition-colors ${selected ? "bg-accent/10" : "hover:bg-surface-muted"}`}>
      <div className="flex items-center gap-3">
        <input
          type="checkbox"
          aria-label={`Select ${note.title}`}
          checked={checked}
          disabled={disabled}
          onChange={() => onChecked(note)}
          className="h-4 w-4 shrink-0 cursor-pointer accent-accent focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-accent"
        />
        <button
          type="button"
          disabled={disabled}
          onClick={() => onSelect(note)}
          aria-pressed={selected}
          className="flex min-w-0 flex-1 items-center gap-3 rounded-lg py-2 text-left focus-visible:outline-2 focus-visible:outline-accent"
        >
          <FiFileText aria-hidden="true" className="shrink-0 text-accent" size={20} />
          <span className="min-w-0 flex-1">
            <span title={note.title} className="block truncate text-sm font-semibold text-text">{note.title}</span>
            <span className="mt-1 block text-xs uppercase tracking-wide text-text-muted">{getNoteFormat(note)}</span>
          </span>
          <FiChevronRight aria-hidden="true" className="shrink-0 text-text-muted" />
        </button>
      </div>
      <div className="ml-7 mt-2">
        <ContentTypeDropDown
          aria-label={`Category for ${note.title}`}
          value={note.resource_type}
          disabled={updating || disabled}
          onChange={(event) => onTypeChange(note, event.target.value as CourseContentType)}
          className="w-full rounded-lg border border-border bg-surface px-2 py-1.5 text-xs text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-60"
        />
        {updating && <span role="status" className="mt-1 block text-xs text-text-muted">Saving category…</span>}
      </div>
    </div>
  );
}
