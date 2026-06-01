import clsx from "clsx";
import type { Thread } from "../../../services";
import { useCallback, useState } from "react";
import { MdOutlineDriveFileRenameOutline } from "react-icons/md";
import { toast } from "react-toastify"
import { useUpdateThread } from "../hooks/hooks";
const chatItemStyle =
    "w-full flex flex-row rounded-md border border-transparent px-3 py-2.5 text-left transition-all duration-base ease-base hover:border-border hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60";

const chatItemActiveStyle = "border-border bg-surface text-text shadow-soft";
const chatItemEditingSelectedStyle = "border-accent bg-surface text-text shadow-soft ring-1 ring-accent/40";
type ThreadBubbleProps = {
    thread: Thread;
    selected: boolean
    onClick: (threadId: string | null) => void;
};
// Could possibly use the store for editing the question, however in this case we are going to 
// to treat this component as stateless
export default function ThreadBubble({ thread, selected, onClick }: ThreadBubbleProps) {
    const [draftTitle, setDraftTitle] = useState(thread.title ?? "New Chat");
    const [isEditing, setIsEditing] = useState(false);
    const [isSaving, setIsSaving] = useState(false);

    const { updateThread } = useUpdateThread()

    const displayTitle = thread.title?.trim() || "New Chat";

    const startEditing = useCallback(() => {
        setDraftTitle(displayTitle);
        setIsEditing(true);
    }, [displayTitle]);

    const cancelEditing = useCallback(() => {
        setDraftTitle(displayTitle);
        setIsEditing(false);
    }, [displayTitle]);

    const confirmEditing = async () => {
        if (!thread.id || isSaving) return;

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

    return (
        <div
            role="button"
            tabIndex={0}
            className={clsx(
                chatItemStyle,
                "flex items-center justify-between gap-2",
                selected && chatItemActiveStyle,
                isEditing && chatItemActiveStyle,
                isEditing && selected && chatItemEditingSelectedStyle
            )}
            onClick={() => !isEditing && onClick(thread.id)}
            onKeyDown={(e) => {
                if (isEditing) return;
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    onClick(thread.id);
                }
            }}
        >
            {isEditing ? (
                <input
                    autoFocus
                    value={draftTitle}
                    disabled={isSaving}
                    className={clsx(
                        "w-full rounded bg-surface-muted px-2 py-1 text-sm text-text",
                        chatItemActiveStyle
                    )}
                    onChange={(e) => setDraftTitle(e.target.value)}
                    onClick={(e) => e.stopPropagation()}
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
                <span className="truncate text-sm text-text">{displayTitle}</span>
            )}

            <button
                type="button"
                aria-label={isEditing ? "Save chat name" : "Rename chat"}
                disabled={isSaving}
                className={clsx(
                    "rounded p-1 text-text-soft hover:bg-surface-muted hover:text-text disabled:cursor-not-allowed disabled:opacity-50",
                    isEditing && "text-accent"
                )}
                onClick={(e) => {
                    e.stopPropagation();
                    if (isEditing) {
                        void confirmEditing();
                        return;
                    }
                    startEditing();
                }}
            >
                <MdOutlineDriveFileRenameOutline />
            </button>
        </div>
    );
}
