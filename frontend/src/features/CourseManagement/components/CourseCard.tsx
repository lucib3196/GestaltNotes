import type { Course } from "../../../services/courses";

type CourseCardProps = {
  course: Course;
  onClick?: (course: Course) => void;
};

export default function CourseCard({ course, onClick }: CourseCardProps) {
  return (
    <button
      type="button"
      onClick={() => onClick?.(course)}
      className="group w-full rounded-lg border border-border bg-surface-muted px-4 py-4 text-left shadow-sm transition-all duration-200 hover:border-accent/70 hover:bg-surface hover:shadow-soft focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="truncate text-base font-semibold text-text">
            {course.name}
          </p>
          <p className="mt-1 text-sm text-text-muted">
            {course.discipline ?? "No discipline set"}
          </p>
        </div>

        <span className="rounded-md border border-border bg-surface px-2.5 py-1 text-xs font-medium text-text-soft transition-colors group-hover:border-accent/50 group-hover:text-text">
          Open
        </span>
      </div>

      <p className="mt-4 text-sm leading-6 text-text-muted">
        {course.description ?? "No description has been added yet."}
      </p>
    </button>
  );
}
