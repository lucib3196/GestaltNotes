import { useState } from "react";
import { MdOutlineDriveFileRenameOutline } from "react-icons/md";
import type { Thread } from "../../../services";
import { useUpdateThread } from "../hooks/hooks";
import { useCallback } from "react";
import { toast } from "react-toastify"

type HeaderProps = {
  thread: Thread | null
}
export function ChatSessionHeader({ thread }: HeaderProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [draftTitle, setDraftTitle] = useState("");
  const [isSaving, setIsSaving] = useState(false);


  const { updateThread } = useUpdateThread()

  const displayTitle = thread?.title?.trim() || "New Chat";

  const startEditing = useCallback(() => {
    setDraftTitle(displayTitle);
    setIsEditing(true);
  }, [displayTitle]);

  const cancelEditing = useCallback(() => {
    setDraftTitle(displayTitle);
    setIsEditing(false);
  }, [displayTitle]);

  const confirmEditing = async () => {
    if (!thread?.id || isSaving) return;

    const nextTitle = draftTitle.trim();
    const fallbackTitle = "New Chat";
    const titleToSave = nextTitle || fallbackTitle;

    // No-op if nothing changed.
    if (titleToSave === displayTitle) {
      setIsEditing(false);
      return;
    }

    try {
      setIsSaving(true);
      await updateThread(thread.id, {
        title: draftTitle
      })
      setIsEditing(false);
    } catch {
      toast.error(
        "Could not rename thread"
      );
    } finally {
      setIsSaving(false);
    }
  }

  // Refrehs 

  return (
    <div className="sticky top-0 z-10 -mx-1 mb-3 border-b border-border bg-surface/95 px-1 pb-2 pt-1 backdrop-blur">
      <div className="flex items-center justify-between gap-2">
        {isEditing ? (
          <input
            autoFocus
            value={draftTitle}
            className="w-full rounded-md border border-border bg-surface-muted px-2 py-1 text-base font-semibold text-text outline-none focus:ring-2 focus:ring-accent/60 sm:text-lg"
            onChange={(e) => setDraftTitle(e.target.value)}
            onBlur={() => void confirmEditing()}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                void confirmEditing();
              }
              if (e.key === "Escape") {
                e.preventDefault();
                cancelEditing();
              }
            }}
          />
        ) : (
          <h1 className="truncate text-base font-semibold text-text sm:text-lg">
            {thread?.title ?? "New Chat"}
          </h1>
        )}

        <button
          type="button"
          onClick={() => {
            if (isEditing) {
              void confirmEditing();
              return;
            }
            startEditing();
          }}
          className="rounded p-1 text-text-soft transition-colors hover:bg-surface-muted hover:text-text"
          aria-label={isEditing ? "Save chat name" : "Edit chat name"}
        >
          <MdOutlineDriveFileRenameOutline />
        </button>
      </div>
    </div>
  );
}
