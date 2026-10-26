import { useRef, useState } from "react";
import {
  useDeleteCourseNote,
  useDownloadCourseNotes,
  useFetchCourseNotes,
  useUpdateCourseNote,
} from "../../../hooks/courses";
import type { CourseContentType, CourseNote } from "../../../services/courses";
import { useCourseDetailsStore } from "../state/useCourseDetailsStore";

export function useCourseResources() {
  const courseId = useCourseDetailsStore((state) => state.selectedCourseId);
  const {
    notes,
    setNotes,
    loading: fetching,
    error: fetchError,
    refetch,
  } = useFetchCourseNotes(courseId);
  const selectedId = useCourseDetailsStore((state) => state.selectedNoteID);
  const selectNote = useCourseDetailsStore((state) => state.selectNote);
  const [checkedIds, setCheckedIds] = useState<string[]>([]);
  const [showUpload, setShowUpload] = useState(false);
  const [busy, setBusy] = useState(false);
  const [updatingIds, setUpdatingIds] = useState<string[]>([]);
  const [actionError, setActionError] = useState<string | null>(null);
  const actionLock = useRef(false);
  const updating = useRef(new Set<string>());
  const { deleteCourseNote } = useDeleteCourseNote();
  const downloadNotes = useDownloadCourseNotes();
  const updateNote = useUpdateCourseNote();
  const checkedNotes = notes.filter((note) => checkedIds.includes(note.id));

  function refreshNotes() {
    void refetch().catch(() => {
      // The fetch hook exposes the error to the list.
    });
  }

  function handleSelect(note: CourseNote) {
    if (actionLock.current) return;
    selectNote(note.id);
  }

  function handleChecked(note: CourseNote) {
    if (actionLock.current) return;
    setCheckedIds((current) =>
      current.includes(note.id)
        ? current.filter((id) => id !== note.id)
        : [...current, note.id],
    );
  }

  async function handleTypeChange(note: CourseNote, type: CourseContentType) {
    if (
      actionLock.current ||
      updating.current.has(note.id) ||
      type === note.resource_type
    )
      return;
    updating.current.add(note.id);
    setUpdatingIds([...updating.current]);
    setActionError(null);
    try {
      const updated = await updateNote(courseId, note.id, type);
      setNotes((current) =>
        current.map((item) => (item.id === note.id ? updated : item)),
      );
    } catch (cause) {
      setActionError(
        `Could not update ${note.title}: ${cause instanceof Error ? cause.message : "Please try again."}`,
      );
    } finally {
      updating.current.delete(note.id);
      setUpdatingIds([...updating.current]);
    }
  }

  async function handleAction(action: "download" | "delete") {
    if (
      actionLock.current ||
      updating.current.size > 0 ||
      checkedNotes.length === 0
    )
      return;
    actionLock.current = true;
    setBusy(true);
    setActionError(null);
    const targets = checkedNotes;
    try {
      const results =
        action === "download"
          ? await downloadNotes(courseId, targets)
          : await Promise.allSettled(
              targets.map((note) => deleteCourseNote(courseId, note.id)),
            );
      const succeeded = new Set(
        targets
          .filter((_, index) => results[index].status === "fulfilled")
          .map((note) => note.id),
      );
      const failed = targets.filter(
        (_, index) => results[index].status === "rejected",
      );
      setCheckedIds((current) => current.filter((id) => !succeeded.has(id)));
      if (action === "delete") {
        setNotes((current) =>
          current.filter((note) => !succeeded.has(note.id)),
        );
        if (selectedId && succeeded.has(selectedId)) {
          selectNote(null);
        }
      }
      if (failed.length > 0) {
        setActionError(
          `Could not ${action}: ${failed.map((note) => note.title).join(", ")}. These files remain selected for retry.`,
        );
      }
    } catch (cause) {
      setActionError(
        cause instanceof Error ? cause.message : `Unable to ${action} files.`,
      );
    } finally {
      actionLock.current = false;
      setBusy(false);
    }
  }

  return {
    notes,
    fetching,
    fetchError,
    selectedId,
    checkedIds,
    setCheckedIds,
    showUpload,
    setShowUpload,
    busy,
    updatingIds,
    actionError,
    checkedNotes,
    refreshNotes,
    handleSelect,
    handleChecked,
    handleTypeChange,
    handleAction,
  };
}
