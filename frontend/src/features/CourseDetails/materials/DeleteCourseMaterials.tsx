import { useCallback, useRef, useState } from "react";
import { createPortal } from "react-dom";

import Modal from "../../../components/Modal/Modal";
import { useDeleteCourseNote } from "../../../hooks/courses";
import type { CourseNoteOverview } from "../../../services/courses";
import { useAuth } from "../../Auth";
import { useCourseDetailsStore } from "../state";
import { activeRun } from "./processingStatus";

type DeleteFailure = { id: string; title: string; message: string };

type Props = {
  onDeleted: (noteIds: string[]) => void;
};

export default function DeleteCourseMaterials({ onDeleted }: Props) {
  const { userData } = useAuth();
  const courseId = useCourseDetailsStore((s) => s.selectedCourseId);
  const checkedIds = useCourseDetailsStore((s) => s.checkedNoteIds);
  const notesById = useCourseDetailsStore((s) => s.notesById);
  const removeNotes = useCourseDetailsStore((s) => s.removeNotes);
  const { deleteCourseNote } = useDeleteCourseNote();
  const [targets, setTargets] = useState<CourseNoteOverview[] | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [failures, setFailures] = useState<DeleteFailure[]>([]);
  const deleteLock = useRef(false);

  const checkedNotes = checkedIds.flatMap((id) => {
    const note = notesById[id];
    return note?.course_id === courseId ? [note] : [];
  });
  const processing = checkedNotes.some((note) =>
    activeRun(note.processing.latest_run?.status),
  );

  const closeModal = useCallback((visible: boolean) => {
    if (!visible && !deleteLock.current) {
      setTargets(null);
      setFailures([]);
    }
  }, []);

  async function confirmDelete() {
    if (!targets?.length || deleteLock.current) return;
    deleteLock.current = true;
    setDeleting(true);
    setFailures([]);
    const succeeded: string[] = [];
    const remaining: CourseNoteOverview[] = [];
    const errors: DeleteFailure[] = [];

    try {
      for (const note of targets) {
        try {
          await deleteCourseNote(note.course_id, note.id);
          succeeded.push(note.id);
        } catch (cause) {
          remaining.push(note);
          errors.push({
            id: note.id,
            title: note.title,
            message: cause instanceof Error ? cause.message : "Could not delete this file.",
          });
        }
      }

      if (succeeded.length) {
        removeNotes(succeeded);
        onDeleted(succeeded);
      }
      setTargets(remaining.length ? remaining : null);
      setFailures(errors);
    } finally {
      deleteLock.current = false;
      setDeleting(false);
    }
  }

  if (!userData?.roles.includes("educator")) return null;

  return (
    <>
      <button
        type="button"
        disabled={!checkedNotes.length || processing || deleting}
        title={processing ? "Wait for selected files to finish processing" : undefined}
        onClick={() => {
          // Freeze the checked targets so confirmation always matches deletion.
          setTargets([...checkedNotes]);
          setFailures([]);
        }}
        className="rounded-lg px-3 py-2 text-xs font-semibold text-red-600 hover:bg-red-500/10 focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-40 dark:text-red-400"
      >
        Delete selected ({checkedNotes.length})
      </button>
      {targets && createPortal(
        <Modal variant="small" setShowModal={closeModal}>
          <h2 className="text-lg font-semibold">
            Delete {targets.length} selected {targets.length === 1 ? "file" : "files"}?
          </h2>
          <ul className="mt-3 max-h-40 list-disc space-y-1 overflow-y-auto pl-5 text-sm">
            {targets.map((note) => <li key={note.id}>{note.title}</li>)}
          </ul>
          <p className="mt-3 text-sm text-text-muted">
            This permanently deletes these uploaded files, their extracted lecture
            materials, and all associated embeddings. This cannot be undone.
          </p>
          {failures.length > 0 && (
            <div role="alert" className="mt-3 space-y-2 text-sm text-red-600 dark:text-red-400">
              <p>These files could not be deleted and remain checked for retry.</p>
              <ul className="space-y-1">
                {failures.map((failure) => (
                  <li key={failure.id}>{failure.title}: {failure.message}</li>
                ))}
              </ul>
            </div>
          )}
          <div className="mt-6 flex justify-end gap-3" aria-busy={deleting}>
            <button type="button" disabled={deleting} onClick={() => closeModal(false)}
              className="rounded-lg border border-border px-4 py-2 text-sm disabled:opacity-40">
              Cancel
            </button>
            <button type="button" disabled={deleting} onClick={() => void confirmDelete()}
              className="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-40">
              {deleting ? "Deleting…" : failures.length ? "Retry failed deletions" : "Delete files"}
            </button>
          </div>
        </Modal>, document.body,
      )}
    </>
  );
}
