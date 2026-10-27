import { useState } from "react";
import { NoteBlocks } from "../../NoteBlocks";
import { useCourseDetailsStore } from "../state/useCourseDetailsStore";
import CourseNotePreview from "./CourseNotePreview";

type WorkspaceMode = "original" | "blocks";

const modes: { value: WorkspaceMode; label: string }[] = [
  { value: "original", label: "Original file" },
  { value: "blocks", label: "Study materials" },
];

export default function StudyWorkspace() {
  const [mode, setMode] = useState<WorkspaceMode>("original");
  const note = useCourseDetailsStore((state) => state.getSelectedNote());
  const courseId = useCourseDetailsStore((state) => state.selectedCourseId);

  if (!note || note.course_id !== courseId) {
    return (
      <section aria-label="Study workspace" className="min-w-0">
        <div className="flex min-h-80 flex-col items-center justify-center px-6 py-12 text-center">
          <h3 className="font-semibold text-text">Study workspace</h3>
          <p className="mt-2 max-w-sm text-sm leading-6 text-text-muted">
            Select a course material to view its original file or study materials.
          </p>
        </div>
      </section>
    );
  }

  const previewKey = `${note.course_id}:${note.id}:${note.file_id}`;
  const latestStatus = note.processing.latest_run?.status;

  const processingMessage = note.processing.has_succeeded
    ? null
    : latestStatus === "partial"
      ? "Processing completed partially. Available study materials are shown below."
      : latestStatus === "queued" ||
          latestStatus === "running" ||
          latestStatus === "retrying"
        ? "Processing is in progress. Some study materials may not be available yet."
        : latestStatus === "failed" || latestStatus === "revoked"
          ? "Processing did not finish. Any available study materials are shown below."
          : "Study materials will appear after this resource is processed.";

  return (
    <section
      aria-label="Study workspace"
      className="min-w-0"
    >
      <header className="space-y-4 border-b border-border p-4 sm:p-5">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-accent">
            Study workspace
          </p>
          <h3 className="mt-1 break-words text-base font-semibold text-text">
            {note.title}
          </h3>
        </div>

        <div role="group" aria-label="Preview mode" className="flex flex-wrap gap-2">
          {modes.map((item) => (
            <button
              key={item.value}
              type="button"
              aria-pressed={mode === item.value}
              onClick={() => setMode(item.value)}
              className={`rounded-lg border px-4 py-2 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent ${
                mode === item.value
                  ? "border-accent bg-accent/10 text-accent"
                  : "border-border bg-surface text-text-muted hover:bg-surface-muted"
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
      </header>

      <div className="min-w-0 p-4 sm:p-5">
        {mode === "original" ? (
          <CourseNotePreview key={previewKey} note={note} />
        ) : (
          <div className="space-y-4">
            {processingMessage && (
              <p className="text-sm text-text-muted">{processingMessage}</p>
            )}
            <NoteBlocks
              key={previewKey}
              courseId={note.course_id}
              fileId={note.file_id}
            />
          </div>
        )}
      </div>
    </section>
  );
}
