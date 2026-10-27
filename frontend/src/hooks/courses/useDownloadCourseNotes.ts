import { useCallback } from "react";
import { useAuth } from "../../features/Auth";
import { CoursesAPI, type CourseNote } from "../../services/courses";

export function useDownloadCourseNotes() {
  const { user } = useAuth();
  return useCallback(async (courseId: string, notes: CourseNote[]) => {
    if (!user) throw new Error("You must be signed in to download notes.");
    const token = await user.getIdToken();
    return Promise.allSettled(notes.map(async (note) => {
      const blob = await CoursesAPI.streamCourseNote(token, courseId, note.id);
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = note.title;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    }));
  }, [user]);
}
