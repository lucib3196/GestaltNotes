import { useCallback, useState } from "react";

import { useAuth } from "../../features/Auth";
import {
  CoursesAPI,
  type CourseContentType,
  type CourseNote,
} from "../../services/courses";

export function useUploadCourseNote() {
  const { user } = useAuth();
  const [note, setNote] = useState<CourseNote | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const uploadCourseNote = useCallback(
    async (courseId: string, file: File, resourceType: CourseContentType) => {
      if (!user) {
        throw new Error("You must be signed in to upload notes.");
      }

      setLoading(true);
      setError(null);

      try {
        const token = await user.getIdToken();
        const uploadedNote = await CoursesAPI.uploadCourseNote(
          token,
          courseId,
          file,
          resourceType,
        );
        setNote(uploadedNote);
        return uploadedNote;
      } catch (err) {
        const error =
          err instanceof Error ? err : new Error("Failed to upload note.");
        setError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [user],
  );

  return { uploadCourseNote, note, loading, error };
}

export type FileResourceMap = {
  file: File;
  resourceType: CourseContentType;
};

type FailedUpload = FileResourceMap & {
  error: Error;
};

export function useUploadMultipleNotes() {
  const { user } = useAuth();
  const [notes, setNotes] = useState<CourseNote[]>([]);
  const [failures, setFailures] = useState<FailedUpload[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const uploadMultipleCourseNotes = useCallback(
    async (courseId: string, files: FileResourceMap[]) => {
      setLoading(true);
      setError(null);
      setNotes([]);
      setFailures([]);

      try {
        if (!user) {
          throw new Error("You must be signed in to upload notes.");
        }

        const token = await user.getIdToken();
        const results = await Promise.allSettled(
          files.map(({ file, resourceType }) =>
            CoursesAPI.uploadCourseNote(
              token,
              courseId,
              file,
              resourceType,
            ),
          ),
        );

        const uploadedNotes: CourseNote[] = [];
        const failedUploads: FailedUpload[] = [];

        results.forEach((result, index) => {
          if (result.status === "fulfilled") {
            uploadedNotes.push(result.value);
          } else {
            failedUploads.push({
              ...files[index],
              error:
                result.reason instanceof Error
                  ? result.reason
                  : new Error("Failed to upload note."),
            });
          }
        });

        setNotes(uploadedNotes);
        setFailures(failedUploads);

        if (failedUploads.length > 0) {
          setError(
            new Error(
              `${failedUploads.length} of ${files.length} uploads failed.`,
            ),
          );
        }

        return { notes: uploadedNotes, failures: failedUploads };
      } catch (cause) {
        const uploadError =
          cause instanceof Error
            ? cause
            : new Error("Failed to upload notes.");

        setError(uploadError);
        throw uploadError;
      } finally {
        setLoading(false);
      }
    },
    [user],
  );

  return { uploadMultipleCourseNotes, notes, failures, loading, error };
}
