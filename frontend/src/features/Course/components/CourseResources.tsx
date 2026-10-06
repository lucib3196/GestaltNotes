import { useEffect, useRef, useState } from "react";
import {
  useFetchCourseNotes,
  useStreamCourseNote,
} from "../../CourseManagement/hooks";
import { FilePreview } from "../../../components/FileAttachments";
import type { CourseNote } from "../../../services/courses";
import { CourseNoteBox } from "./CourseNoteBox";

export function CourseResources({ courseId }: { courseId: string }) {
  // Remount selection and requests when navigating to another course.
  return <ResourceContent key={courseId} courseId={courseId} />;
}

function Header({ size }: { size: number }) {
  return (
    <div className="flex items-center justify-between border-b border-border px-4 py-4">
      <h2 className="font-semibold text-text">Resources</h2>
      <span className="text-sm text-text-muted">{size} files</span>
    </div>
  );
}

function ResourceContent({ courseId }: { courseId: string }) {
  const {
    notes,
    loading: fetching,
    error: fetchError,
    refetch,
  } = useFetchCourseNotes(courseId);
  const [selected, setSelected] = useState<CourseNote | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const selection = useRef(0);
  const { streamCourseNote, cancel, loading, error } = useStreamCourseNote();

  useEffect(
    () => () => {
      selection.current += 1;
    },
    [],
  );

  const handleSelect = async (note: CourseNote) => {
    const request = ++selection.current;
    setSelected(note);
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
      // The hook exposes the current request error for the preview panel.
    }
  };

  const handleCancel = () => {
    selection.current += 1;
    cancel();
  };

  return (
    <div className="flex flex-row">
      <section
        aria-label="Course resources"
        className="min-w-0 overflow-hidden rounded-xl border border-border bg-surface"
      >
        {fetching ? (
          <p role="status" className="p-4 text-sm text-text-muted">
            Loading resources…
          </p>
        ) : fetchError ? (
          <div role="alert" className="p-4 text-sm text-text-muted">
            <p>{fetchError.message}</p>
            <button
              type="button"
              onClick={() => {
                void refetch().catch(() => {});
              }}
              className="mt-2 text-accent underline"
            >
              Try again
            </button>
          </div>
        ) : notes.length === 0 ? (
          <p className="p-4 text-sm text-text-muted">
            No resources have been uploaded yet.
          </p>
        ) : (
          <ul className="max-h-144 divide-y divide-border overflow-y-auto">
            {notes.map((note) => (
              <li key={note.id}>
                <CourseNoteBox
                  note={note}
                  selected={selected?.id === note.id}
                  onSelect={(note) => {
                    void handleSelect(note);
                  }}
                />
              </li>
            ))}
          </ul>
        )}
      </section>

      <section
        aria-label="Resource preview"
        aria-busy={loading}
        className="min-w-0 w-full"
      >
        {selected ? (
          <>
            {loading ? (
              <div className="flex items-center justify-between gap-4 py-8">
                <p role="status" className="text-sm text-text-muted">
                  Opening resource…
                </p>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="rounded-lg border border-border px-3 py-2 text-sm text-text"
                >
                  Cancel
                </button>
              </div>
            ) : error ? (
              <div role="alert" className="py-6 text-sm text-text-muted">
                <p>{error.message}</p>
                <button
                  type="button"
                  onClick={() => {
                    void handleSelect(selected);
                  }}
                  className="mt-3 text-accent underline"
                >
                  Try again
                </button>
              </div>
            ) : file ? (
              <FilePreview file={file} showDownload />
            ) : (
              <div className="py-8 text-sm text-text-muted">
                <p>Loading cancelled.</p>
                <button
                  type="button"
                  onClick={() => {
                    void handleSelect(selected);
                  }}
                  className="mt-3 text-accent underline"
                >
                  Open resource
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="flex min-h-64 flex-col items-center justify-center gap-2 text-center">
            <h2 className="font-semibold text-text">Preview a resource</h2>
            <p className="text-sm text-text-muted">
              Select a file to view its contents or download it.
            </p>
          </div>
        )}
      </section>
    </div>
  );
}
