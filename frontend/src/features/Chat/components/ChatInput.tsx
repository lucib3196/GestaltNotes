import clsx from "clsx";
import React, { useMemo, useState, useRef, type JSX } from "react";
import { IoCloseCircle } from "react-icons/io5";
import { UploadImagesChat } from "./UploadImagesChat";

type ChatInputVariant = "default" | "subtle";

const VariantClasses: Record<
  ChatInputVariant,
  {
    root: string;
    preview: string;
    toolbar: string;
    newButton: string;
    input: string;
    sendButton: string;
  }
> = {
  default: {
    root: "rounded-xl border border-border bg-surface p-2",
    preview: "mb-2 w-full rounded-xl border border-border bg-surface-muted p-2",
    toolbar: "mt-0 flex w-full items-end gap-2 border-t border-border pt-3",
    newButton:
      "rounded-md border border-border px-3 py-2 text-sm text-text-muted transition-colors duration-base ease-base hover:bg-surface-muted hover:text-text",
    input:
      "flex-1 rounded-md border border-border bg-surface-strong px-3 py-2.5 text-sm text-text outline-none placeholder:text-text-soft focus:border-border-strong focus:ring-2 focus:ring-accent/50",
    sendButton:
      "rounded-md bg-accent px-3.5 py-2.5 text-sm font-semibold text-bg transition-all duration-base ease-base hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50",
  },
  subtle: {
    root: "rounded-xl border border-border bg-surface-muted p-2",
    preview: "mb-2 w-full rounded-xl border border-border bg-surface p-2",
    toolbar: "mt-0 flex w-full items-end gap-2 pt-3",
    newButton:
      "rounded-md border border-border px-3 py-2 text-sm text-text-muted transition-colors duration-base ease-base hover:bg-surface hover:text-text",
    input:
      "flex-1 rounded-md border border-border bg-surface px-3 py-2.5 text-sm text-text outline-none placeholder:text-text-soft focus:border-border-strong focus:ring-2 focus:ring-accent/50",
    sendButton:
      "rounded-md bg-accent px-3.5 py-2.5 text-sm font-semibold text-bg transition-all duration-base ease-base hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50",
  },
};

export interface ChatInputProps {
  handleSubmit: (val: string, images?: string[]) => Promise<void>;
  disabled: boolean;
  multiModal?: boolean;
  variant?: ChatInputVariant;
  toolbar?: React.ReactNode | JSX.Element;
}

export default function ChatInput({
  handleSubmit,
  disabled,
  multiModal = true,
  variant = "default",
  toolbar
}: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const styles = VariantClasses[variant];
  const previews = useMemo(
    () => files.map((file) => ({ file, url: URL.createObjectURL(file) })),
    [files],
  );

  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  const onMessageChange = (val: string) => {
    setMessage(val);
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "0px";
    el.style.height = `${Math.min(el.scrollHeight, 220)}px`; // max height
  };

  const submit = () => {
    const trimmed = message.trim();
    if (!trimmed || disabled) return;
    const images = previews.map((v) => v.url);
    handleSubmit(trimmed, images.length > 0 ? images : undefined);
    setFiles([]);
    setMessage("");
  };

  function onFileSelect(files: File[]) {
    setFiles((prev) => [...prev, ...files]);
  }

  return (
    <div className={clsx("flex flex-col", styles.root)}>
      {previews.length > 0 ? (
        <div className={clsx(styles.preview, "grid w-full grid-cols-2 gap-2 sm:grid-cols-3")}>
          {previews.map(({ file: f, url }) => (
            <div
              key={`${f.name}-${f.lastModified}-${f.size}`}
              className="group relative overflow-hidden rounded-lg border border-border bg-surface p-1"
            >
              <button
                type="button"
                aria-label={`Remove ${f.name}`}
                onClick={() => setFiles((prev) => prev.filter((v) => v !== f))}
                className="absolute right-2 top-2 z-10 rounded-full border border-border bg-surface-strong text-text-muted transition-all duration-base ease-base hover:scale-105 hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
              >
                <IoCloseCircle className="h-5 w-5" />
              </button>
              <img
                src={url}
                alt={f.name || "Preview"}
                className="h-28 w-full rounded-md object-cover sm:h-32"
              />
              <div className="truncate px-1 pt-1 text-xs text-text-soft">{f.name}</div>
            </div>
          ))}
        </div>
      ) : null}

      <div className={styles.toolbar}>
        {multiModal && <UploadImagesChat onFilesSelected={onFileSelect} />}
        <textarea
          ref={textareaRef}
          className={clsx(styles.input, "min-h-10 max-h-55 resize-none overflow-y-auto")}
          placeholder="Type a message..."
          disabled={disabled}
          value={message}
          rows={1}
          onChange={(e) => onMessageChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              submit();
            }
          }}
        />
        <div className="flex items-center justify-between gap-3 p-2">


          <button
            type="button"
            onClick={submit}
            disabled={disabled || !message.trim()}
            className={clsx(
              styles.sendButton,
              "min-w-22 rounded-lg px-4 py-2 text-sm font-semibold transition-all",
              "enabled:hover:-translate-y-0.5 enabled:hover:shadow-sm",
              "disabled:cursor-not-allowed disabled:opacity-50"
            )}
          >
            Send
          </button>
          {toolbar ? (
            <div className="flex items-center gap-2 text-sm text-text-muted">{toolbar}</div>
          ) : (
            <div />
          )}
        </div>
      </div>
    </div>
  );
}
