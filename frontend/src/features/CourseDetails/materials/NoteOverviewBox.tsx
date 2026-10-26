import type { CourseNoteOverview } from "../../../services/courses";
import {
  useNoteProcessing,
  type RefreshNote,
} from "../hooks/useNoteProcessing";
import { CourseNoteCard } from "../ui/CourseNoteCard";
import { CourseNoteDetails } from "../ui/CourseNoteDetails";
import { ProcessingActions } from "./ui/ProcessingActions";
import { ProcessingBadge } from "./ui/ProcessingBadge";
import { useCourseDetailsStore } from "../state";
export function NoteOverviewBox({
  note,
  onRefresh,
}: {
  note: CourseNoteOverview;
  onRefresh: RefreshNote;
}) {
  const processing = useNoteProcessing(note, onRefresh);
  const checkedIds = useCourseDetailsStore((s) => s.checkedNoteIds);
  const selected = useCourseDetailsStore((s) => s.selectedNoteID);
  const selectNote = useCourseDetailsStore((s) => s.selectNote);
  const toggle = useCourseDetailsStore((s) => s.toggleCheckedNote);

  const checked = checkedIds.includes(note.id);

  return (
    <CourseNoteCard>
      <div className="flex items-center gap-3">
        <input
          type="checkbox"
          aria-label={`Select ${note.title}`}
          checked={checked}
          onChange={() => toggle(note.id)}
          className="h-4 w-4 shrink-0 cursor-pointer accent-accent focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-accent"
        />
        <button
          type="button"
          onClick={() => selectNote(note.id)}
          aria-pressed={selected == note.id}
          className="flex min-w-0 flex-1 items-center gap-3 rounded-lg py-2 text-left focus-visible:outline-2 focus-visible:outline-accent"
        >
          <CourseNoteDetails note={note} />
        </button>
        <div className="ml-8 mt-2 flex flex-wrap items-center justify-between gap-3">
          <span className="text-xs capitalize text-text-muted">
            {note.resource_type}
          </span>
          <div className="flex flex-wrap items-center justify-end gap-2">
            <ProcessingBadge status={processing.status} />
            <ProcessingActions {...processing.actions} />
          </div>
        </div>
      </div>
    </CourseNoteCard>
  );
}
