import { useState } from "react";

import { useChatContext } from "../instance";
import { MdOutlineDriveFileRenameOutline } from "react-icons/md";

export function ChatSessionHeader() {
  const currentThread = useChatContext((s) => s.thread);
  const updateThread = useChatContext((s) => s.updateThread);

  const [isEditing, setIsEditing] = useState(false);
  const [draftTitle, setDraftTitle] = useState("");

  const startEditing = () => {
    setDraftTitle(currentThread?.title ?? "New Chat");
    setIsEditing(true);
  };

  const cancelEditing = () => {
    setIsEditing(false);
    setDraftTitle("");
  };

  const confirmEditing = async () => {
    if (!currentThread?.id) return cancelEditing;

    const nextTitle = draftTitle.trim();
    if (!nextTitle || nextTitle === (currentThread.title ?? "").trim()) {
      return cancelEditing();
    }

    await updateThread(currentThread.id, { title: nextTitle });
    cancelEditing();
  };

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
            {currentThread?.title ?? "New Chat"}
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