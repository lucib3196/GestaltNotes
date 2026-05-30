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

export type UploadFileSize = "sm" | "md" | "lg" | "full";

// Base styles shared by upload surfaces.
export const uploadFilesBase =
  "mx-auto flex w-full cursor-pointer flex-col items-center justify-center p-8 text-center transition-colors focus-within:outline-none focus-within:ring-2 focus-within:ring-accent/60";

export type UploadFilesStyle = "outline" | "solid" | "ghost" | "editor";
export const UploadFilesStyles: Record<UploadFilesStyle, string> = {
  outline: clsx(
    "rounded-lg border-2 border-dashed border-border bg-surface",
    "hover:border-border-strong hover:bg-surface-muted",
  ),
  solid: clsx(
    "rounded-lg border border-transparent bg-accent text-bg",
    "hover:opacity-90",
  ),
  ghost: clsx(
    "rounded-lg border border-transparent bg-transparent text-text-muted",
    "hover:bg-surface-muted hover:text-text",
  ),
  editor: clsx(
    "rounded-lg border border-border-strong bg-code text-text",
    "hover:border-accent focus-within:ring-accent/60",
  ),
};

export const UploadFilesSize: Record<UploadFileSize, string> = {
  sm: "max-w-sm",
  md: "max-w-md",
  lg: "max-w-lg",
  full: "w-full",
};

type UploadFilesProp = {
  onFilesSelected: (files: File[]) => void;
  variant?: UploadFilesStyle;
  size?: UploadFileSize;
  // Optional helper message describing what files users should upload.
  message?: string;
  // Whether the picker should allow selecting multiple files at once.
  multiple?: boolean;
  // Which file types are accepted by this upload control.
  accept?: UploadAccept;
};

export function UploadImagesChat({
  onFilesSelected,
  multiple = true,
  accept = "images",
}: UploadFilesProp) {
  const inputId = "chat-upload-input";

  return (
    <>
      <input
        type="file"
        accept={acceptMap[accept]}
        id={inputId}
        className="sr-only"
        multiple={multiple}
        onChange={(e) => {
          const files = e.target.files ? Array.from(e.target.files) : [];
          onFilesSelected(files);
          e.currentTarget.value = "";
        }}
      />

      <label
        htmlFor={inputId}
        aria-label="Upload files"
        title="Upload image"
        className={clsx(
          "group inline-flex h-10 w-10 cursor-pointer items-center justify-center rounded-md",
          "border border-border bg-surface text-text-muted shadow-sm",
          "transition-all duration-base ease-base",
          "hover:border-border-strong hover:bg-surface-muted hover:text-text",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60",
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
