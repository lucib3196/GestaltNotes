import { Link, useParams } from "react-router-dom";
import { useGetCourse } from "../../hooks/courses";
import CourseHeader from "./components/CourseHeader";
import { CourseResources } from "./components/CourseResources";

export default function CourseDetails() {
  const { courseId } = useParams();
  const { course, loading, error, refetch } = useGetCourse(courseId);

  return (
    <main className="mx-auto w-full max-w-7xl space-y-8 px-4 py-8 sm:px-6 lg:px-8">
      <Link
        to="/educator/courses"
        className="text-sm font-medium text-text-muted hover:text-accent"
      >
        ← My courses
      </Link>
      {loading ? (
        <p role="status">Loading course…</p>
      ) : error ? (
        <div role="alert">
          <p>{error.message}</p>
          <button
            type="button"
            onClick={() => void refetch().catch(() => { })}
            className="mt-3 text-accent underline"
          >
            Try again
          </button>
        </div>
      ) : course ? (
        <>
          <CourseHeader
            key={course.id}
            course={course}
            refetch={() => void refetch().catch(() => { })}
          />
          <CourseResources courseId={course.id} />
        </>
      ) : (
        <p>Course not found.</p>
      )}
    </main>
  );
}
