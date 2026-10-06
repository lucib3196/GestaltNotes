import { useRef, useState } from "react";
import { EyeIcon, XMarkIcon } from "@heroicons/react/24/outline";
import {
  FileBox,
  FilePreview,
  FileUpload,
  UploadButton,
} from "../../../components/FileAttachments";
import type { SupportedContentType } from "../../../services/courses/types";
import { useUploadCourseNote } from "../../CourseManagement/hooks";
import { ContentTypeDropDown } from "./ContentTypeDropDown";

type PendingCourseNote = {
  id: string;
  file: File;
  resourceType: SupportedContentType;
};

export default function CourseNoteUpload({
  courseID,
  reFetch,
}: {
  courseID?: string | null;
  reFetch?: () => void;
}) {
  const [items, setItems] = useState<PendingCourseNote[]>([]);
  const [previewID, setPreviewID] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const uploadInProgress = useRef(false);
  const { uploadCourseNote } = useUploadCourseNote();

  function handleFilesChange(files: File[]) {
    setError(null);
    setItems((current) => [
      ...current,
      ...files.map((file) => ({
        id: crypto.randomUUID(),
        file,
        resourceType: "notes" as const,
      })),
    ]);
  }

  function updateResourceType(id: string, resourceType: SupportedContentType) {
    setItems((current) =>
      current.map((item) =>
        item.id === id ? { ...item, resourceType } : item,
      ),
    );
  }

  function handleRemove(id: string) {
    setItems((current) => current.filter((item) => item.id !== id));
    setPreviewID((current) => (current === id ? null : current));
  }

  async function handleUpload() {
    if (!courseID || items.length === 0 || uploadInProgress.current) return;
    uploadInProgress.current = true;
    setUploading(true);
    setError(null);

    try {
      // Preserve failed and unattempted files so the user can retry.
      for (const item of items) {
        await uploadCourseNote(courseID, item.file, item.resourceType);
        handleRemove(item.id);
      }
    } catch (cause) {
      setError(
        cause instanceof Error ? cause.message : "Failed to upload files.",
      );
    } finally {
      uploadInProgress.current = false;
      setUploading(false);
      reFetch?.();
    }
  }

  const actionClassName =
    "inline-flex h-10 w-10 items-center justify-center rounded-lg " +
    "text-text-soft transition-colors hover:bg-surface-muted hover:text-text " +
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent " +
    "disabled:cursor-not-allowed disabled:opacity-50";

  return (
    <section aria-label="Course files" className="space-y-8 text-text">
      <header>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-soft">
          Course resources
        </p>
        <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">
            Course files
          </h2>
          <p role="status" className="text-sm text-text-soft">
            {items.length} {items.length === 1 ? "file" : "files"} selected
          </p>
        </div>
        <p className="mt-3 text-base text-text-soft">
          Keep your notes and course materials in one place.
        </p>
      </header>

      <FileUpload
        variant="dropzone"
        multiple
        disabled={uploading || !courseID}
        onFilesChange={handleFilesChange}
      />

      {items.length > 0 && (
        <section aria-labelledby="pending-files-heading">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <h3 id="pending-files-heading" className="text-lg font-semibold">
              Ready to upload
            </h3>
            <p className="text-sm text-text-soft">
              Choose a category for each file
            </p>
          </div>
          <ul className="divide-y divide-border border-b border-border">
            {items.map((item) => (
              <li key={item.id} className="py-5">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
                  <div className="min-w-0 flex-1">
                    <FileBox file={item.file} />
                  </div>
                  <div className="flex items-center gap-2">
                    <ContentTypeDropDown
                      value={item.resourceType}
                      disabled={uploading}
                      aria-label={`Category for ${item.file.name}`}
                      onChange={(event) =>
                        updateResourceType(
                          item.id,
                          event.target.value as SupportedContentType,
                        )
                      }
                    />
                    <button
                      type="button"
                      aria-label={`Preview ${item.file.name}`}
                      aria-expanded={previewID === item.id}
                      aria-controls={`preview-${item.id}`}
                      title="Preview file"
                      className={actionClassName}
                      onClick={() =>
                        setPreviewID((current) =>
                          current === item.id ? null : item.id,
                        )
                      }
                    >
                      <EyeIcon aria-hidden="true" className="h-5 w-5" />
                    </button>
                    <button
                      type="button"
                      disabled={uploading}
                      aria-label={`Remove ${item.file.name}`}
                      title="Remove file"
                      className={actionClassName}
                      onClick={() => handleRemove(item.id)}
                    >
                      <XMarkIcon aria-hidden="true" className="h-5 w-5" />
                    </button>
                  </div>
                </div>
                <div id={`preview-${item.id}`} hidden={previewID !== item.id}>
                  {previewID === item.id && (
                    <FilePreview file={item.file} showDownload />
                  )}
                </div>
              </li>
            ))}
          </ul>
        </section>
      )}

      {error && (
        <p role="alert" className="text-sm text-text">
          {error} Successfully uploaded files have been removed. Remaining files
          are ready to retry.
        </p>
      )}
      {!courseID && (
        <p className="text-sm text-text-soft">
          Select a course before uploading files.
        </p>
      )}
      <UploadButton
        items={items}
        handleUpload={handleUpload}
        uploading={uploading}
        disabled={!courseID}
      />
    </section>
  );
}
