import MarkdownRenderer from "../../../components/Markdown/MarkdownRenderer";
import { useState } from "react";
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  Description,
} from "@headlessui/react";
import { FiSend, FiUsers, FiX } from "react-icons/fi";
import type { Announcement } from "../../../services/announcements";
import { useAnnouncementActions, useAnnouncementAudience } from "../hooks";

export default function PublishAnnouncementDialog({
  announcement,
  onClose,
  onPublished,
}: {
  announcement: Announcement;
  onClose: () => void;
  onPublished: (announcement: Announcement) => void;
}) {
  const [target, setTarget] = useState<
    "all" | "student" | "educator" | "assigned"
  >("all");
  const role =
    target === "student" || target === "educator" ? target : undefined;
  const audience = useAnnouncementAudience(announcement.id, role);
  const actions = useAnnouncementActions();
  const count =
    target === "assigned"
      ? audience.data?.existing_recipients
      : audience.data?.total_users;
  const blocked =
    actions.pending ||
    audience.loading ||
    Boolean(audience.error) ||
    !audience.data ||
    !count ||
    audience.data.published ||
    (role !== undefined && audience.data.conflicting_recipients > 0);
  async function publish() {
    if (blocked) return;
    try {
      const published =
        target === "assigned"
          ? await actions.publish(announcement.id)
          : await actions.publishToAll(
              announcement.id,
              role ? [role] : undefined,
            );
      onPublished(published);
    } catch {
      /* The action hook exposes the error below. */
    }
  }
  return (
    <Dialog
      open
      onClose={() => {
        if (!actions.pending) onClose();
      }}
      className="relative z-50"
    >
      <div
        className="fixed inset-0 bg-black/65 backdrop-blur-sm"
        aria-hidden="true"
      />
      <div className="fixed inset-0 flex items-center justify-center overflow-y-auto p-4">
        <DialogPanel className="max-h-[90dvh] w-full max-w-xl overflow-y-auto rounded-2xl border border-border bg-surface-strong p-6 shadow-soft sm:p-8">
          <div className="flex items-start justify-between gap-4">
            <div className="rounded-xl bg-accent/10 p-3 text-accent">
              <FiSend size={24} aria-hidden="true" />
            </div>
            <button
              type="button"
              aria-label="Close publish dialog"
              onClick={onClose}
              disabled={actions.pending}
              className="rounded-lg p-2 text-text-muted hover:bg-surface-muted disabled:opacity-50"
            >
              <FiX size={20} />
            </button>
          </div>
          <DialogTitle className="mt-5 text-2xl font-semibold">
            Ready to share?
          </DialogTitle>
          <Description className="mt-2 text-sm leading-6 text-text-muted">
            Review your saved announcement and choose who will receive it in the
            app.
          </Description>
          <div className="mt-5 rounded-xl border border-border bg-bg p-4">
            <p className="font-mono text-xs text-text-soft">
              v{announcement.version}
            </p>
            <h3 className="mt-2 break-words font-semibold">
              {announcement.title}
            </h3>
            <div className="mt-2 max-h-40 min-w-0 overflow-y-auto break-words text-sm leading-6">
              <MarkdownRenderer>{announcement.message}</MarkdownRenderer>
            </div>
          </div>
          <fieldset disabled={actions.pending} className="mt-5 space-y-3">
            <legend className="mb-3 text-sm font-semibold">Audience</legend>
            {(
              [
                {
                  value: "all",
                  label: "All current users",
                  description:
                    "Includes everyone on the app at publication time. Future signups won’t be added.",
                },
                {
                  value: "student",
                  label: "All current students",
                  description:
                    "Only users with the student role at publication time.",
                },
                {
                  value: "educator",
                  label: "All current educators",
                  description:
                    "Only users with the educator role at publication time.",
                },
                {
                  value: "assigned",
                  label: "Assigned recipients only",
                  description:
                    "Publish to the users already assigned to this announcement.",
                },
              ] as const
            ).map((option) => (
              <label
                key={option.value}
                className="flex cursor-pointer items-start gap-3 rounded-xl border border-border p-4"
              >
                <input
                  type="radio"
                  name="audience"
                  value={option.value}
                  checked={target === option.value}
                  onChange={() => setTarget(option.value)}
                  className="mt-1 accent-cyan-400"
                />
                <span>
                  <span className="block text-sm font-medium">
                    {option.label}
                  </span>
                  <span className="mt-1 block text-xs leading-5 text-text-muted">
                    {option.description}
                  </span>
                </span>
              </label>
            ))}
          </fieldset>
          {audience.loading && (
            <p role="status" className="mt-4 text-sm text-text-muted">
              Checking audience…
            </p>
          )}
          {audience.data && (
            <div className="mt-4 flex items-center gap-3 rounded-xl bg-accent/10 p-4 text-accent">
              <FiUsers size={22} aria-hidden="true" />
              <div>
                <p className="font-semibold">
                  {count?.toLocaleString()}{" "}
                  {count === 1 ? "recipient" : "recipients"}
                </p>
                <p className="mt-1 text-xs text-text-muted">
                  {target === "assigned"
                    ? "Existing recipients will see the published announcement."
                    : `${audience.data.existing_recipients} already assigned · ${audience.data.new_recipients} to add`}
                </p>
              </div>
            </div>
          )}
          <p className="mt-3 text-xs leading-5 text-text-soft">
            Audience counts may change before publishing. Delivery is in-app.
          </p>
          {role &&
            audience.data &&
            audience.data.conflicting_recipients > 0 && (
              <p
                role="alert"
                className="mt-4 rounded-xl border border-red-400/30 p-3 text-sm text-red-300"
              >
                {audience.data.conflicting_recipients} existing{" "}
                {audience.data.conflicting_recipients === 1
                  ? "recipient is"
                  : "recipients are"}{" "}
                outside the selected role. Remove those recipients or choose all
                users before publishing. No announcement will be sent while this
                conflict remains.
              </p>
            )}
          {audience.data?.published && (
            <p role="alert" className="mt-3 text-sm text-text-muted">
              This announcement has already been published. Refresh the
              dashboard.
            </p>
          )}
          {count === 0 && (
            <p role="alert" className="mt-3 text-sm text-text-muted">
              There are no recipients for this audience.
            </p>
          )}
          {(audience.error || actions.error) && (
            <div
              role="alert"
              className="mt-4 rounded-xl border border-red-400/30 p-3 text-sm text-red-300"
            >
              <p>{actions.error?.message || audience.error?.message}</p>
              {audience.error && (
                <button
                  type="button"
                  onClick={() => void audience.refetch()}
                  className="mt-2 underline"
                >
                  Retry audience preview
                </button>
              )}
            </div>
          )}
          <div className="mt-6 flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={actions.pending}
              className="rounded-xl border border-border px-4 py-2.5 text-sm disabled:opacity-50"
            >
              Keep as draft
            </button>
            <button
              type="button"
              onClick={() => void publish()}
              disabled={Boolean(blocked)}
              className="inline-flex items-center gap-2 rounded-xl bg-accent px-5 py-2.5 text-sm font-semibold text-bg hover:bg-accent-strong disabled:cursor-not-allowed disabled:opacity-50"
            >
              <FiSend aria-hidden="true" />
              {actions.pending ? "Publishing…" : "Publish announcement"}
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  );
}
