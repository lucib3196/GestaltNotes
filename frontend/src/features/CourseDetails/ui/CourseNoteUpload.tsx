import { useRef, useState } from "react";
import { useShallow } from "zustand/react/shallow";
import { XMarkIcon } from "@heroicons/react/24/outline";
import {
  FileBox,
  FileUpload,
  UploadButton,
} from "../../../components/FileAttachments";
import { useUploadCourseNote } from "../../../hooks/courses";
import type { CourseContentType } from "../../../services/courses";
import { ContentTypeDropDown } from "../../CourseNote/components/ContentTypeDropDown";
import { useCourseDetailsStore } from "../state";
type Props = {
  onUploaded: () => Promise<unknown>;
};

export default function CourseNoteUpload({ onUploaded }: Props) {
  const { courseID, files, addFiles, removeFile, updateResourceType } =
    useCourseDetailsStore(
      useShallow((state) => ({
        courseID: state.selectedCourseId,
        files: state.items,
        addFiles: state.addFiles,
        removeFile: state.removeFile,
        updateResourceType: state.updateResourceType,
      })),
    );

  const { uploadCourseNote } = useUploadCourseNote();
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const uploadInProgress = useRef(false);

  async function handleUpload() {
    if (!courseID || files.length === 0 || uploadInProgress.current) return;

    uploadInProgress.current = true;
    setUploading(true);
    setError(null);

    try {
      for (const item of files) {
        await uploadCourseNote(courseID, item.file, item.resourceType);
        removeFile(item.id);
      }
    } catch (cause) {
      setError(
        cause instanceof Error ? cause.message : "Failed to upload notes.",
      );
    } finally {
      try {
        await onUploaded();
      } catch {
        setError("Could not refresh course materials. Try refreshing the list.");
      } finally {
        uploadInProgress.current = false;
        setUploading(false);
      }
    }
  }

  return (
    <section
      aria-label="Upload course notes"
      aria-busy={uploading}
      className="space-y-4 text-text"
    >
      

      <FileUpload
        variant="dropzone"
        multiple
        disabled={uploading || !courseID}
        onFilesChange={addFiles}
      />

      {files.length > 0 && (
        <ul className="divide-y divide-border">
          {files.map((item) => (
            <li
              key={item.id}
              className="flex flex-col gap-3 py-4 sm:flex-row sm:items-center"
            >
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
                      event.target.value as CourseContentType,
                    )
                  }
                />

                <button
                  type="button"
                  disabled={uploading}
                  aria-label={`Remove ${item.file.name}`}
                  onClick={() => removeFile(item.id)}
                  className="rounded-lg p-2 text-text-soft hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50"
                >
                  <XMarkIcon aria-hidden="true" className="h-5 w-5" />
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {error && (
        <p role="alert" className="text-sm">
          {error} Remaining files are ready to retry.
        </p>
      )}

      {!courseID && (
        <p className="text-sm text-text-soft">
          Select a course before uploading notes.
        </p>
      )}

      <UploadButton
        items={files}
        handleUpload={handleUpload}
        uploading={uploading}
        disabled={!courseID}
      />
    </section>
  );
}
