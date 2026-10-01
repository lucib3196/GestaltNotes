import clsx from "clsx";
import { useState } from "react";

export type FileUploadVariant = "compact" | "panel" | "dropzone";

export type FileUploadItem<TType extends string> = {
  file: File;
  resourceType: TType;
};

type FileUploadProps<TType extends string> = {
  resourceTypes: readonly TType[];
  defaultResourceType: TType;
  variant?: FileUploadVariant;
  multiple?: boolean;
  uploading?: boolean;
  onUpload: (items: FileUploadItem<TType>[]) => Promise<void> | void;
};

const variantClassName: Record<FileUploadVariant, string> = {
  compact: "rounded-lg border border-border bg-surface p-4",
  panel: "rounded-xl border border-border bg-surface p-5 shadow-soft",
  dropzone:
    "rounded-xl border-2 border-dashed border-border bg-surface-muted p-6 text-center",
};

export default function FileUpload<TType extends string>({
  resourceTypes,
  defaultResourceType,
  variant = "panel",
  multiple = true,
  uploading = false,
  onUpload,
}: FileUploadProps<TType>) {
  const [items, setItems] = useState<FileUploadItem<TType>[]>([]);

  function handleFiles(files: FileList | null) {
    if (!files) return;

    setItems(
      Array.from(files).map((file) => ({
        file,
        resourceType: defaultResourceType,
      })),
    );
  }

  function updateResourceType(index: number, resourceType: TType) {
    setItems((current) =>
      current.map((item, itemIndex) =>
        itemIndex === index ? { ...item, resourceType } : item,
      ),
    );
  }

  async function handleUpload() {
    await onUpload(items);
    setItems([]);
  }

  const hasFiles = items.length > 0;

  return (
    <section className={variantClassName[variant]}>
      <input
        type="file"
        multiple={multiple}
        accept=".pdf,.doc,.docx,.ppt,.pptx,.txt"
        
        onChange={(event) => handleFiles(event.target.files)}
        className={clsx(
          "block w-full rounded-lg border border-border bg-surface-strong px-3 py-2 text-sm text-text",
          "file:mr-4 file:rounded-md file:border-0 file:bg-accent file:px-3 file:py-1.5 file:text-sm file:font-semibold file:text-bg",
        )}
      />

      {hasFiles && (
        <div className="mt-4 grid gap-3">
          {items.map((item, index) => (
            <div
              key={`${item.file.name}-${index}`}
              className="rounded-lg border border-border bg-surface-muted p-3 text-left"
            >
              <p className="truncate text-sm font-semibold text-text">
                {item.file.name}
              </p>
              <p className="mt-1 text-xs text-text-soft">
                {(item.file.size / 1024).toFixed(1)} KB
              </p>

              <select
                value={item.resourceType}
                onChange={(event) =>
                  updateResourceType(index, event.target.value as TType)
                }
                className="mt-3 w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text outline-none focus:border-accent focus:ring-2 focus:ring-accent/35"
              >
                {resourceTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>
      )}

      <button
        type="button"
        disabled={!hasFiles || uploading}
        onClick={handleUpload}
        className="mt-4 rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-bg transition-colors hover:bg-accent-strong disabled:cursor-not-allowed disabled:opacity-60"
      >
        {uploading ? "Uploading..." : "Upload files"}
      </button>
    </section>
  );
}
