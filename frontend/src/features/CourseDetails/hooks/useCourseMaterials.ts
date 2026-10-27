import { useCallback } from "react";
import { useAuth } from "../../Auth";
import { useFetchCourseNotesOverview } from "../../../hooks/courses/useFetchCourseNotes";
import { CoursesAPI, type CourseNoteOverview } from "../../../services/courses";
import { useCourseDetailsStore } from "../state/useCourseDetailsStore";

export function useCourseMaterials() {
  const courseId = useCourseDetailsStore((state) => state.selectedCourseId);
  const { user } = useAuth();
  const { notes, setNotes, loading, error, refetch } =
    useFetchCourseNotesOverview(courseId);

  const refreshNote = useCallback(
    async (note: CourseNoteOverview) => {
      if (!user) throw new Error("You must be signed in to check processing.");
      const token = await user.getIdToken();
      const updated = await CoursesAPI.getCourseNoteOverview(
        token,
        note.course_id,
        note.id,
      );
      setNotes((current) =>
        current.map((item) => (item.id === updated.id ? updated : item)),
      );
      return updated;
    },
    [user, setNotes],
  );

  return { notes, loading, error, refetch, refreshNote };
}
