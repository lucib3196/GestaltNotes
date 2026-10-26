import { useEffect, useState } from "react";
import { FilePreview } from "../../../components/FileAttachments";
import { useStreamCourseNote } from "../../../hooks/courses";
import type { CourseNoteOverview } from "../../../services/courses";
import { useCourseDetailsStore } from "../state/useCourseDetailsStore";

export default function CourseNotePreview() {
  const note = useCourseDetailsStore((state) => state.getSelectedNote());

  return (
    <section aria-label="Resource preview" className="grow">
      {note ? (
        <SelectedNotePreview key={`${note.id}:${note.file_id}`} note={note} />
      ) : (
        <div className="flex min-h-80 flex-col items-center justify-center rounded-2xl bg-surface-muted/40 px-6 text-center">
          <h3 className="font-semibold text-text">Preview a resource</h3>
          <p className="mt-2 max-w-sm text-sm leading-6 text-text-muted">
            Select a course material to preview its file.
          </p>
        </div>
      )}
    </section>
  );
}

function SelectedNotePreview({ note }: { note: CourseNoteOverview }) {
  const { streamCourseNote, cancel, error } = useStreamCourseNote();
  const [file, setFile] = useState<File | null>(null);
  const [cancelled, setCancelled] = useState(false);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let active = true;

    async function load() {
      try {
        const blob = await streamCourseNote(note.course_id, note.id);
        if (!active || !blob) return;

        setFile(
          new File([blob], note.title, {
            type: note.content_type || blob.type || "application/octet-stream",
          }),
        );
      } catch {
        // The stream hook exposes the request error.
      }
    }

    queueMicrotask(() => {
      if (active) void load();
    });

    return () => {
      active = false;
      cancel();
    };
  }, [
    note.course_id,
    note.id,
    note.title,
    note.content_type,
    streamCourseNote,
    cancel,
    attempt,
  ]);

  function retry() {
    setFile(null);
    setCancelled(false);
    setAttempt((value) => value + 1);
  }

  if (error) {
    return (
      <div role="alert" className="py-8 text-sm text-text-muted">
        <p>{error.message}</p>
        <button
          type="button"
          onClick={retry}
          className="mt-3 text-accent underline"
        >
          Try again
        </button>
      </div>
    );
  }

  if (file) return <FilePreview file={file} showDownload />;

  if (cancelled) {
    return (
      <div className="py-8 text-sm text-text-muted">
        <p>Loading cancelled.</p>
        <button
          type="button"
          onClick={retry}
          className="mt-3 text-accent underline"
        >
          Open resource
        </button>
      </div>
    );
  }

  return (
    <div
      aria-busy="true"
      className="flex min-h-40 items-center justify-between gap-4 py-8"
    >
      <p role="status" className="text-sm text-text-muted">
        Opening {note.title}…
      </p>
      <button
        type="button"
        onClick={() => {
          cancel();
          setCancelled(true);
        }}
        className="rounded-lg px-3 py-2 text-sm text-accent hover:bg-accent/10"
      >
        Cancel
      </button>
    </div>
  );
}
