import { FiDownload, FiTrash2, FiX } from "react-icons/fi";

type Props = {
  count: number;
  busy: boolean;
  onDownload: () => void;
  onDelete: () => void;
  onClear: () => void;
};

const buttonClass =
  "inline-flex items-center gap-1.5 rounded-lg px-2 py-2 text-xs font-semibold transition-colors hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50";

export function ResourceActions({
  count,
  busy,
  onDownload,
  onDelete,
  onClear,
}: Props) {
  return (
    <div
      className="mb-3 rounded-md bg-surface-muted p-3"
      aria-label="Selected file actions"
    >
      <p role="status" className="text-xs font-medium text-text-muted">
        {busy ? "Working…" : `${count} selected`}
      </p>
      <div className="mt-1 flex flex-wrap items-center gap-1">
        <button
          type="button"
          disabled={busy}
          onClick={onDownload}
          className={buttonClass}
        >
          <FiDownload aria-hidden="true" /> Download
        </button>
        <button
          type="button"
          disabled={busy}
          onClick={onDelete}
          className={buttonClass}
        >
          <FiTrash2 aria-hidden="true" /> Delete
        </button>
        <button
          type="button"
          disabled={busy}
          onClick={onClear}
          className={buttonClass}
        >
          <FiX aria-hidden="true" /> Clear
        </button>
      </div>
    </div>
  );
}
