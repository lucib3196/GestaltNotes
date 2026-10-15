import { FilePreview } from "../../../components/FileAttachments";
import type { CourseNote } from "../../../services/courses";

type Props = {
  note: CourseNote | null;
  file: File | null;
  loading: boolean;
  error: Error | null;
  onCancel: () => void;
  onRetry: () => void;
};

export function ResourcePreview({ note, file, loading, error, onCancel, onRetry }: Props) {
  return (
    <section
      aria-label="Resource preview"
      aria-busy={loading}
      className="min-w-0 lg:sticky lg:top-16 lg:self-start"
    >
      {!note ? (
        <div className="flex min-h-80 flex-col items-center justify-center rounded-2xl bg-surface-muted/40 px-6 text-center">
          <h3 className="font-semibold text-text">Preview a resource</h3>
          <p className="mt-2 max-w-sm text-sm leading-6 text-text-muted">
            Click a filename to preview it. Use the checkboxes to download or delete files.
          </p>
        </div>
      ) : loading ? (
        <div className="flex min-h-40 items-center justify-between gap-4 py-8">
          <p role="status" className="text-sm text-text-muted">Opening {note.title}…</p>
          <button
            type="button"
            onClick={onCancel}
            className="rounded-lg px-3 py-2 text-sm text-accent hover:bg-accent/10"
          >Cancel</button>
        </div>
      ) : error ? (
        <div role="alert" className="py-8 text-sm text-text-muted">
          <p>{error.message}</p>
          <button type="button" onClick={onRetry} className="mt-3 text-accent underline">Try again</button>
        </div>
      ) : file ? (
        <FilePreview file={file} showDownload />
      ) : (
        <div className="py-8 text-sm text-text-muted">
          <p>Loading cancelled.</p>
          <button type="button" onClick={onRetry} className="mt-3 text-accent underline">Open resource</button>
        </div>
      )}
    </section>
  );
}
