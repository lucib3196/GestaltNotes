import { CreateCourse } from "./components";
import { useFetchMyCourses } from "./hooks";

export default function CourseManagement() {
  const { courses, refetch } = useFetchMyCourses();

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
        <div className="mt-4 grid gap-3">
          {courses.map((course) => (
            <article
              key={course.id}
              className="rounded-lg border border-border bg-surface-muted px-4 py-3"
            >
              <p className="font-semibold text-text">{course.name}</p>
              <p className="mt-1 text-sm text-text-muted">
                {course.discipline ?? "No discipline set"}
              </p>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
