import { useId, useRef, useState, type FormEvent } from "react";
import { MdOutlineDriveFileRenameOutline } from "react-icons/md";
import type { Thread } from "../../../../services";
import { useUpdateThread } from "../../hooks/useUpdateThread";
import { useChatStore } from "../../instance";

type HeaderProps = { thread: Thread | null };

export function ChatSessionHeader({ thread }: HeaderProps) {
  return <HeaderContent key={thread?.id ?? "new-chat"} thread={thread} />;
}

function HeaderContent({ thread }: HeaderProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [draftTitle, setDraftTitle] = useState("");
  const [saveError, setSaveError] = useState<string | null>(null);
  const submitting = useRef(false);
  const inputId = useId();
  const errorId = useId();
  const { updateThread, loading } = useUpdateThread();
  const upsertThread = useChatStore((state) => state.upsertThread);
  const displayTitle = thread?.title?.trim() || "New chat";
  const nextTitle = draftTitle.trim();
  const canSave = nextTitle.length > 0 && nextTitle !== displayTitle && !loading;
  const buttonStyle = "inline-flex min-h-9 items-center justify-center rounded-md px-3 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 disabled:cursor-not-allowed disabled:opacity-50";

  function cancelEditing() {
    if (submitting.current) return;
    setIsEditing(false);
    setSaveError(null);
  }

  async function saveTitle(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!thread || !canSave || submitting.current) return;
    submitting.current = true;
    setSaveError(null);
    try {
      const updated = await updateThread(thread.id, { title: nextTitle });
      if (!updated) {
        setSaveError("Please sign in to rename this chat.");
        return;
      }
      upsertThread(updated);
      setIsEditing(false);
    } catch {
      setSaveError("Could not save the title. Please try again.");
    } finally {
      submitting.current = false;
    }
  }

  return (
    <header className="shrink-0 border-b border-border bg-surface px-4 py-3 text-text sm:px-6">
      <div className="mx-auto max-w-5xl">
        <p className="mb-1 text-xs font-medium uppercase tracking-wider text-text-soft">Conversation</p>
        {isEditing ? (
          <form onSubmit={saveTitle} className="space-y-2" aria-label="Rename conversation">
            <div className="flex flex-wrap items-center gap-2">
              <label htmlFor={inputId} className="sr-only">Chat title</label>
              <input
                id={inputId}
                autoFocus
                required
                value={draftTitle}
                disabled={loading}
                onFocus={(event) => event.currentTarget.select()}
                onChange={(event) => {
                  setDraftTitle(event.target.value);
                  setSaveError(null);
                }}
                onKeyDown={(event) => {
                  if (event.key === "Escape") {
                    event.preventDefault();
                    cancelEditing();
                  }
                  if (event.key === "Enter" && event.nativeEvent.isComposing) event.preventDefault();
                }}
                aria-invalid={Boolean(saveError)}
                aria-describedby={saveError ? errorId : undefined}
                className="min-w-0 basis-full rounded-md border border-border bg-surface-strong px-3 py-2 text-base font-semibold outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60 sm:flex-1 sm:basis-auto"
              />
              <button type="submit" disabled={!canSave} className={`${buttonStyle} bg-accent text-white dark:text-code hover:opacity-90`}>
                {loading ? "Saving…" : "Save"}
              </button>
              <button type="button" disabled={loading} onClick={cancelEditing} className={`${buttonStyle} text-text-muted hover:bg-surface-muted hover:text-text`}>Cancel</button>
            </div>
            {saveError ? <p id={errorId} role="alert" className="text-sm text-red-500">{saveError}</p> : <p className="text-xs text-text-soft">Enter to save · Escape to cancel</p>}
          </form>
        ) : (
          <div className="flex min-w-0 items-center justify-between gap-3">
            <h1 title={displayTitle} className="min-w-0 truncate text-base font-semibold sm:text-lg">{displayTitle}</h1>
            <button
              type="button"
              disabled={!thread}
              onClick={() => {
                setDraftTitle(displayTitle);
                setSaveError(null);
                setIsEditing(true);
              }}
              aria-label="Edit chat title"
              title={thread ? "Edit chat title" : "Send a message to start this chat"}
              className={`${buttonStyle} shrink-0 text-text-muted hover:bg-surface-muted hover:text-text`}
            >
              <MdOutlineDriveFileRenameOutline aria-hidden="true" className="h-5 w-5" />
              <span className="ml-2 hidden sm:inline">Rename</span>
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
