import { useEffect, useRef, useState } from "react";
import { FiPlus } from "react-icons/fi";
import {
  useDeleteCourseNote,
  useDownloadCourseNotes,
  useFetchCourseNotes,
  useStreamCourseNote,
  useUpdateCourseNote,
} from "../../../hooks/courses";
import type { CourseContentType, CourseNote } from "../../../services/courses";
import Modal from "../../../components/Modal/Modal";
import CourseNoteUpload from "../../CourseNote/components/CourseNoteUpload";
import { CourseNoteBox } from "./CourseNoteBox";
import { ResourceActions } from "./ResourceActions";
import { ResourcePreview } from "./ResourcePreview";
import { useCourseDetailsStore } from "../instance";

export function CourseResources() {
  const courseId = useCourseDetailsStore((state) => state.selectedCourseId);
  const {
    notes,
    setNotes,
    loading: fetching,
    error: fetchError,
    refetch,
  } = useFetchCourseNotes(courseId);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [checkedIds, setCheckedIds] = useState<string[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [showUpload, setShowUpload] = useState(false);
  const [busy, setBusy] = useState(false);
  const [updatingIds, setUpdatingIds] = useState<string[]>([]);
  const [actionError, setActionError] = useState<string | null>(null);
  const actionLock = useRef(false);
  const updating = useRef(new Set<string>());
  const selection = useRef(0);
  const { streamCourseNote, cancel, loading, error } = useStreamCourseNote();
  const { deleteCourseNote } = useDeleteCourseNote();
  const downloadNotes = useDownloadCourseNotes();
  const updateNote = useUpdateCourseNote();
  const selected = notes.find((note) => note.id === selectedId) ?? null;
  const checkedNotes = notes.filter((note) => checkedIds.includes(note.id));

  useEffect(
    () => () => {
      selection.current += 1;
    },
    [],
  );

  function refreshNotes() {
    void refetch().catch(() => {
      // The fetch hook exposes the error to the list.
    });
  }

  async function handleSelect(note: CourseNote) {
    if (actionLock.current) return;
    const request = ++selection.current;
    setSelectedId(note.id);
    setFile(null);
    try {
      const blob = await streamCourseNote(courseId, note.id);
      if (!blob || selection.current !== request) return;
      setFile(
        new File([blob], note.title, {
          type: note.content_type || blob.type || "application/octet-stream",
        }),
      );
    } catch {
      // The preview hook exposes the error.
    }
  }

  function handleCancel() {
    selection.current += 1;
    cancel();
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
          handleCancel();
          setSelectedId(null);
          setFile(null);
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

  return (
    <section aria-labelledby="course-resources-heading" className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2
            id="course-resources-heading"
            className="text-xl font-semibold text-text"
          >
            Course resources
          </h2>
          <p className="mt-1 text-sm text-text-muted">
            {notes.length} files · Notes, lectures, and supporting materials
          </p>
        </div>
        <button
          type="button"
          onClick={() => setShowUpload(true)}
          disabled={busy || updatingIds.length > 0}
          className="inline-flex items-center gap-2 rounded-xl bg-accent px-4 py-2.5 text-sm font-semibold text-bg transition-colors hover:bg-accent-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 disabled:opacity-50"
        >
          <FiPlus aria-hidden="true" /> Upload notes
        </button>
      </header>
      {showUpload && (
        <Modal setShowModal={setShowUpload}>
          <CourseNoteUpload reFetch={refreshNotes} />
        </Modal>
      )}
      {actionError && (
        <p
          role="alert"
          className="rounded-lg bg-surface-muted p-3 text-sm text-text"
        >
          {actionError}
        </p>
      )}
      <div className="grid items-start gap-6 lg:grid-cols-[22rem_minmax(0,1fr)]">
        <div aria-label="Course resources" className="min-w-0">
          <ResourceActions
            count={checkedNotes.length}
            busy={busy || updatingIds.length > 0}
            onDownload={() => void handleAction("download")}
            onDelete={() => void handleAction("delete")}
            onClear={() => setCheckedIds([])}
          />

          {fetching ? (
            <p role="status" className="p-4 text-sm text-text-muted">
              Loading resources…
            </p>
          ) : fetchError ? (
            <div role="alert" className="p-4 text-sm text-text-muted">
              <p>{fetchError.message}</p>
              <button
                type="button"
                onClick={refreshNotes}
                className="mt-2 text-accent underline"
              >
                Try again
              </button>
            </div>
          ) : notes.length === 0 ? (
            <p className="rounded-xl bg-surface-muted/40 p-6 text-sm text-text-muted">
              No files yet. Upload notes to start building your course library.
            </p>
          ) : (
            <ul className="space-y-1 lg:max-h-[75vh] lg:overflow-y-auto scrollbar-hide">
              {notes.map((note) => (
                <li key={note.id}>
                  <CourseNoteBox
                    note={note}
                    selected={selectedId === note.id}
                    checked={checkedIds.includes(note.id)}
                    updating={updatingIds.includes(note.id)}
                    disabled={busy}
                    onSelect={(item) => void handleSelect(item)}
                    onChecked={handleChecked}
                    onTypeChange={(item, type) =>
                      void handleTypeChange(item, type)
                    }
                  />
                </li>
              ))}
            </ul>
          )}
        </div>
        <ResourcePreview
          note={selected}
          file={file}
          loading={loading}
          error={error}
          onCancel={handleCancel}
          onRetry={() => {
            if (selected) void handleSelect(selected);
          }}
        />
      </div>
    </section>
  );
}
