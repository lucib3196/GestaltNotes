import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { useGetCourse } from "../../hooks/courses";
import CourseHeader from "./ui/CourseHeader";
import StudyWorkspace from "./ui/StudyWorkspace";
import { CourseDetailsProvider, useCourseDetailsStore } from "./state";
import CourseMaterials from "./materials/CourseMaterials";
import CourseNoteUpload from "./ui/CourseNoteUpload";
import { useCourseMaterials } from "./hooks/useCourseMaterials";
import { useState } from "react";
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
  const [showUpload, setShowUpload] = useState<boolean>(false);

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
          <div>
            <button
              type="button"
              onClick={() => setShowUpload(prev=>!prev)}
              className="rounded-lg border border-border bg-surface px-4 py-2 text-sm font-medium text-text transition-colors hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
            >
              Upload notes
            </button>
          </div>
          {showUpload && <CourseNoteUpload onUploaded={materials.refetch} />}
          <div className="grid min-w-0 overflow-hidden rounded-2xl border border-border bg-surface lg:grid-cols-[20rem_minmax(0,1fr)]">
            <div className="min-w-0 border-b border-border bg-surface-muted/20 p-4 lg:border-b-0 lg:border-r">
              <CourseMaterials materials={materials} />
            </div>
            <StudyWorkspace />
          </div>
        </>
      ) : (
        <p>Course not found.</p>
      )}
    </main>
  );
}
