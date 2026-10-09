import { useId, useRef, useState, type FormEvent } from "react";
import type { Thread } from "../../../../services";
import { useUpdateThread } from "../../hooks/useUpdateThread";

export type RenameThreadFormProps = {
  thread: Thread;
  onClose: () => void;
  onRenamed: (thread: Thread) => void;
};

export default function RenameThreadForm({
  thread,
  onClose,
  onRenamed,
}: RenameThreadFormProps) {
  const inputId = useId();
  const errorId = useId();
  const [title, setTitle] = useState(thread.title ?? "");
  const [saveError, setSaveError] = useState<string | null>(null);
  const submitting = useRef(false);
  const { updateThread, loading } = useUpdateThread();
  const nextTitle = title.trim();
  const canSave = nextTitle.length > 0 &&
    nextTitle !== (thread.title ?? "").trim() && !loading;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSave || submitting.current) return;
    submitting.current = true;
    setSaveError(null);
    try {
      const updated = await updateThread(thread.id, { title: nextTitle });
      if (!updated) {
        setSaveError("Please sign in to rename this chat.");
        return;
      }
      onClose();
      onRenamed(updated);
    } catch {
      setSaveError("Could not rename this chat. Please try again.");
    } finally {
      submitting.current = false;
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="space-y-1">
        <h2 className="text-lg font-semibold text-text">Rename chat</h2>
        <p className="text-sm text-text-soft">
          Choose a title that makes this conversation easy to find.
        </p>
      </div>
      <div className="space-y-2">
        <label htmlFor={inputId} className="block text-sm font-medium text-text">
          Chat title
        </label>
        <input
          id={inputId}
          autoFocus
          required
          value={title}
          disabled={loading}
          onChange={(event) => {
            setTitle(event.target.value);
            setSaveError(null);
          }}
          aria-invalid={Boolean(saveError)}
          aria-describedby={saveError ? errorId : undefined}
          placeholder="Enter a chat title"
          className="w-full rounded-lg border border-border bg-surface px-3 py-2.5 text-sm text-text outline-none placeholder:text-text-soft focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60"
        />
        {saveError && (
          <p id={errorId} role="alert" className="text-sm text-red-500">{saveError}</p>
        )}
      </div>
      <div className="flex justify-end gap-2 border-t border-border/40 pt-4">
        <button
          type="button"
          onClick={onClose}
          disabled={loading}
          className="rounded-md px-4 py-2 text-sm font-medium text-text-soft hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 disabled:opacity-50"
        >Cancel</button>
        <button
          type="submit"
          disabled={!canSave}
          className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-bg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 disabled:cursor-not-allowed disabled:opacity-50"
        >{loading ? "Saving…" : "Save"}</button>
      </div>
    </form>
  );
}
