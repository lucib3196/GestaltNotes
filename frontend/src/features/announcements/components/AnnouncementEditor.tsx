import { useState, type FormEvent } from "react";
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  Description,
} from "@headlessui/react";
import { FiX } from "react-icons/fi";
import type {
  Announcement,
  AnnouncementCreate,
} from "../../../services/announcements";
import { useAnnouncementActions } from "../hooks";
import AnnouncementPreview from "./AnnouncementPreview";
interface Props {
  announcement: Announcement | null;
  onClose: () => void;
  onSaved: (announcement: Announcement) => void;
}
const inputClass =
  "mt-2 w-full rounded-xl border border-border bg-bg px-4 py-3 text-sm text-text outline-none focus:border-accent focus:ring-1 focus:ring-accent disabled:opacity-60";

export default function AnnouncementEditor({
  announcement,
  onClose,
  onSaved,
}: Props) {
  const [title, setTitle] = useState(announcement?.title ?? "");
  const [message, setMessage] = useState(announcement?.message ?? "");
  const [version, setVersion] = useState(announcement?.version ?? "");
  const { create, update, pending, error } = useAnnouncementActions();
  const [validationError, setValidationError] = useState<string | null>(null);
  const dirty =
    title !== (announcement?.title ?? "") ||
    message !== (announcement?.message ?? "") ||
    version !== (announcement?.version ?? "");
  function close() {
    if (!pending && (!dirty || window.confirm("Discard your unsaved changes?")))
      onClose();
  }
  async function save(event: FormEvent) {
    event.preventDefault();
    const data: AnnouncementCreate = {
      title: title.trim(),
      message: message.trim(),
      version: version.trim(),
    };
    if (!data.title || !data.message || !data.version) {
      setValidationError("Add a title, message, and version before saving.");
      return;
    }
    setValidationError(null);
    try {
      const saved = announcement
        ? await update(announcement.id, data)
        : await create(data);
      onSaved(saved);
    } catch {
      /* The action hook exposes the error below. */
    }
  }
  return (
    <Dialog open onClose={close} className="relative z-50">
      <div
        className="fixed inset-0 bg-black/65 backdrop-blur-sm"
        aria-hidden="true"
      />
      <div className="fixed inset-0 overflow-y-auto p-3 sm:p-8">
        <div className="flex min-h-full items-center justify-center">
          <DialogPanel className="w-full max-w-5xl rounded-2xl border border-border bg-surface-strong p-5 shadow-soft sm:p-8">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-widest text-accent">
                  Announcement studio
                </p>
                <DialogTitle className="mt-2 text-2xl font-semibold">
                  {announcement ? "Edit announcement" : "Create announcement"}
                </DialogTitle>
                <Description className="mt-2 text-sm text-text-muted">
                  {announcement?.published
                    ? "Changes will update the announcement users already see."
                    : "Save a draft, review your audience, then publish when you’re ready."}
                </Description>
              </div>
              <button
                type="button"
                onClick={close}
                disabled={pending}
                aria-label="Close editor"
                className="rounded-lg p-2 text-text-muted hover:bg-surface-muted focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50"
              >
                <FiX size={22} />
              </button>
            </div>
            <form onSubmit={save} className="mt-7">
              <div className="grid gap-7 md:grid-cols-2">
                <fieldset disabled={pending} className="min-w-0 space-y-5">
                  <label className="block text-sm font-medium">
                    Title
                    <input
                      autoFocus
                      required
                      maxLength={150}
                      value={title}
                      onChange={(event) => setTitle(event.target.value)}
                      placeholder="What’s new in Gestalt Notes?"
                      className={inputClass}
                    />
                    <span className="mt-1 block text-right text-xs text-text-soft">
                      {title.length}/150
                    </span>
                  </label>
                  <label className="block text-sm font-medium">
                    App version
                    <input
                      required
                      maxLength={50}
                      value={version}
                      onChange={(event) => setVersion(event.target.value)}
                      placeholder="e.g. 1.2.0"
                      className={inputClass}
                    />
                  </label>

                  <label className="block text-sm font-medium">
                    Message
                    <textarea
                      required
                      maxLength={5000}
                      rows={8}
                      value={message}
                      onChange={(event) => setMessage(event.target.value)}
                      placeholder="Tell your users what changed and why it matters…"
                      className={`${inputClass} resize-y leading-6`}
                    />
                  </label>
                  <p className="text-xs text-text-soft">
                    Markdown supported: headings, **bold**, lists, links, and
                    tables.
                  </p>
                  <span className="mt-1 block text-right text-xs text-text-soft">
                    {message.length}/5,000
                  </span>
                </fieldset>
                <AnnouncementPreview
                  title={title}
                  message={message}
                  version={version}
                />
              </div>
              {(error || validationError) && (
                <p
                  role="alert"
                  className="mt-5 rounded-xl border border-red-400/30 bg-red-400/10 px-4 py-3 text-sm text-red-300"
                >
                  {validationError || error?.message}
                </p>
              )}
              <div className="mt-7 flex flex-wrap justify-end gap-3 border-t border-border pt-5">
                <button
                  type="button"
                  onClick={close}
                  disabled={pending}
                  className="rounded-xl border border-border px-5 py-2.5 text-sm font-medium disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={pending || Boolean(announcement && !dirty)}
                  className="rounded-xl bg-accent px-5 py-2.5 text-sm font-semibold text-bg hover:bg-accent-strong disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {pending
                    ? "Saving…"
                    : announcement
                      ? "Save changes"
                      : "Save draft"}
                </button>
              </div>
            </form>
          </DialogPanel>
        </div>
      </div>
    </Dialog>
  );
}
