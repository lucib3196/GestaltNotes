import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { useGetCourse } from "../../hooks/courses";
import CourseHeader from "./ui/CourseHeader";
import CourseNotePreview from "./ui/CourseNotePreview";
import { CourseDetailsProvider, useCourseDetailsStore } from "./state";
import CourseMaterials from "./materials/CourseMaterials";
import CourseNoteUpload from "./ui/CourseNoteUpload";
import { useCourseMaterials } from "./hooks/useCourseMaterials";

export default function CourseDetails() {
  const { courseId } = useParams();
  if (!courseId) return <p>Course not found.</p>;

  return (
    <CourseDetailsProvider key={courseId} courseId={courseId}>
      <CourseDetailsContent />
    </CourseDetailsProvider>
  );
}

function CourseDetailsContent() {
  const courseId = useCourseDetailsStore((state) => state.selectedCourseId);
  const selectedCourse = useCourseDetailsStore((state) => state.selectedCourse);
  const setSelectedCourse = useCourseDetailsStore(
    (state) => state.setSelectedCourse,
  );
  const { course, loading, error, refetch } = useGetCourse(courseId);
  const materials = useCourseMaterials();

  useEffect(() => {
    let active = true;
    queueMicrotask(() => {
      if (active && course) setSelectedCourse(course);
    });
    return () => {
      active = false;
    };
  }, [course, setSelectedCourse]);

  return (
    <main className="mx-auto w-full  space-y-8 px-4 py-8 sm:px-6 lg:px-8">
      <Link
        to="/educator/courses"
        className="text-sm font-medium text-text-muted hover:text-accent"
      >
        ← My courses
      </Link>
      {loading || (!error && course && !selectedCourse) ? (
        <p role="status">Loading course…</p>
      ) : error ? (
        <div role="alert">
          <p>{error.message}</p>
          <button
            type="button"
            onClick={() => void refetch().catch(() => {})}
            className="mt-3 text-accent underline"
          >
            Try again
          </button>
        </div>
      ) : selectedCourse ? (
        <>
          <CourseHeader />
          <CourseNoteUpload onUploaded={materials.refetch} />
          <div className="flex flex-row gap-2 px-2 py-3">
            <CourseMaterials materials={materials} />
            <CourseNotePreview />
          </div>
        </>
      ) : (
        <p>Course not found.</p>
      )}
    </main>
  );
}
