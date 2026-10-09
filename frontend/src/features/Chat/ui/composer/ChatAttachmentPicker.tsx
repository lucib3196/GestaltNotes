import { useId } from "react";
import clsx from "clsx";
import { CiCirclePlus } from "react-icons/ci";

export type UploadAccept = "images" | "pdf" | "images_pdf" | "any" | "zip";

export const acceptMap: Record<UploadAccept, string> = {
  images: "image/*",
  pdf: "application/pdf",
  images_pdf: "image/*,application/pdf",
  zip: ".zip,application/zip",
  any: "*",
};

type ChatAttachmentPickerProps = {
  onFilesSelected: (files: File[]) => void;
  multiple?: boolean;
  accept?: UploadAccept;
  disabled?: boolean;
};

export function ChatAttachmentPicker({
  onFilesSelected,
  multiple = true,
  accept = "images",
  disabled = false,
}: ChatAttachmentPickerProps) {
  const inputId = useId();

  return (
    <>
      <input
        type="file"
        accept={acceptMap[accept]}
        id={inputId}
        className="peer sr-only"
        multiple={multiple}
        disabled={disabled}
        aria-label="Attach files"
        onChange={(e) => {
          const files = e.target.files ? Array.from(e.target.files) : [];
          onFilesSelected(files);
          e.currentTarget.value = "";
        }}
      />

      <label
        htmlFor={inputId}
        aria-label="Attach files"
        title="Attach files"
        className={clsx(
          "group inline-flex h-10 w-10 items-center justify-center rounded-md",
          "border border-border bg-surface text-text-muted shadow-sm",
          "transition-all duration-base ease-base",
          "hover:border-border-strong hover:bg-surface-muted hover:text-text",
          "peer-focus-visible:ring-2 peer-focus-visible:ring-accent/60",
          disabled ? "cursor-not-allowed opacity-50" : "cursor-pointer",
        )}
      >
        <CiCirclePlus
          size={22}
          className="transition-transform duration-base ease-base group-hover:scale-105"
        />
      </label>
    </>
  );
}
