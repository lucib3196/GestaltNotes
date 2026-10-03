import { useNavigate } from "react-router-dom";

import { CourseCard, CreateCourse } from "./components";
import { useFetchMyCourses } from "./hooks";

export default function CourseManagement() {
  const navigate = useNavigate();
  const { courses, loading, error, refetch } = useFetchMyCourses();

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-4 py-8 sm:px-6 lg:px-8">
      <header>
        <h1 className="text-3xl font-bold text-text">Courses</h1>
        <p className="mt-2 text-sm text-text-muted">
          Create and manage the courses connected to your teaching workspace.
        </p>
      </header>

      <CreateCourse onCreated={() => void refetch()} />

      <section className="rounded-xl border border-border bg-surface p-5">
        <h2 className="text-lg font-semibold text-text">My Courses</h2>

        {loading && (
          <p className="mt-4 text-sm text-text-muted">Loading courses...</p>
        )}

        {error && <p className="mt-4 text-sm text-red-400">{error.message}</p>}

        <div className="mt-4 grid gap-3">
          {courses.map((course) => (
            <CourseCard
              key={course.id}
              course={course}
              onClick={(selectedCourse) =>
                navigate(`/educator/courses/${selectedCourse.id}`)
              }
            />
          ))}
        </div>
      </section>
    </div>
  );
}
