import { useCallback } from "react";
import { useAuth } from "../../features/Auth";
import { CoursesAPI, type CourseContentType } from "../../services/courses";

export function useUpdateCourseNote() {
  const { user } = useAuth();
  return useCallback(async (courseId: string, noteId: string, resourceType: CourseContentType) => {
    if (!user) throw new Error("You must be signed in to update notes.");
    const token = await user.getIdToken();
    return CoursesAPI.updateCourseNote(token, courseId, noteId, { resource_type: resourceType });
  }, [user]);
}
