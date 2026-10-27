import clsx from "clsx";
import { useRef, useState } from "react";
import { CloudArrowUpIcon } from "@heroicons/react/24/outline";

export type FileUploadVariant = "compact" | "panel" | "dropzone";

type FileUploadProps = {
  variant?: FileUploadVariant;
  multiple?: boolean;
  onFilesChange: (files: File[]) => void;
  disabled?: boolean;
};

const ACCEPT = ".pdf,.doc,.docx,.ppt,.pptx,.txt";
const EXTENSIONS = new Set(ACCEPT.split(","));

export default function FileUpload({
  variant = "panel",
  multiple = true,
  onFilesChange,
  disabled = false,
}: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleFiles(files: FileList | null) {
    if (!files || disabled) return;
    const selected = Array.from(files);
    const supported = selected.filter((file) => {
      const extension = "." + file.name.split(".").pop()?.toLowerCase();
      return EXTENSIONS.has(extension);
    });
    setError(
      supported.length !== selected.length
        ? "Some files were skipped. Choose PDF, Word, PowerPoint, or TXT files."
        : null,
    );
    if (supported.length > 0) {
      onFilesChange(multiple ? supported : supported.slice(0, 1));
    }
  }

  return (
    <section
      aria-label="Choose files to upload"
      onDragOver={(event) => {
        event.preventDefault();
        if (!disabled) setDragging(true);
      }}
      onDragLeave={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget as Node | null)) {
          setDragging(false);
        }
      }}
      onDrop={(event) => {
        event.preventDefault();
        setDragging(false);
        handleFiles(event.dataTransfer.files);
      }}
      className={clsx(
        "rounded-xl border bg-surface-muted text-center",
        variant === "dropzone"
          ? "border-2 border-dashed px-6 py-10 sm:py-12"
          : variant === "panel"
            ? "p-5 shadow-soft"
            : "p-4",
        dragging && !disabled ? "border-accent" : "border-border",
        disabled && "opacity-60",
      )}
    >
      <input
        ref={inputRef}
        type="file"
        aria-label="Choose course files"
        disabled={disabled}
        multiple={multiple}
        accept={ACCEPT}
        className="hidden"
        onChange={(event) => {
          handleFiles(event.target.files);
          event.target.value = "";
        }}
      />
      {variant === "dropzone" && (
        <>
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-surface-strong">
            <CloudArrowUpIcon aria-hidden="true" className="h-7 w-7 text-accent" />
          </div>
          <h3 className="mt-5 text-xl font-semibold text-text">
            Drop your course files here
          </h3>
          <p className="mt-3 text-base text-text-soft">
            or choose files from your device
          </p>
        </>
      )}
      <button
        type="button"
        disabled={disabled}
        onClick={() => inputRef.current?.click()}
        className={clsx(
          "rounded-xl border border-border bg-surface px-6 py-3",
          "font-semibold text-text hover:border-accent",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent",
          "disabled:cursor-not-allowed",
          variant === "dropzone" && "mt-6",
        )}
      >
        Browse files
      </button>
      <p className="mt-3 text-xs text-text-soft">
        PDF, Word, PowerPoint, and TXT
      </p>
      {error && <p role="alert" className="mt-3 text-sm text-text">{error}</p>}
    </section>
  );
}
