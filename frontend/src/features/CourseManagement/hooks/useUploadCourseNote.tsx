import { useCallback, useState } from "react";

import { useAuth } from "../../Auth";
import { CoursesAPI, type CourseNote } from "../../../services/courses";

export function useUploadCourseNote() {
  const { user } = useAuth();
  const [note, setNote] = useState<CourseNote | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const uploadCourseNote = useCallback(
    async (courseId: string, file: File) => {
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
