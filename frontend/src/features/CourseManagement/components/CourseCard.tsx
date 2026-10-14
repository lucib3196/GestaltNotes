import { FiArrowUpRight, FiBookOpen } from "react-icons/fi";
import type { Course } from "../../../services/courses";

type CourseCardProps = {
  course: Course;
  onClick?: (course: Course) => void;
};

export default function CourseCard({ course, onClick }: CourseCardProps) {
  return (
    <button type="button" onClick={() => onClick?.(course)} className="group flex h-full w-full flex-col rounded-2xl border border-border bg-surface p-6 text-left transition-colors hover:border-accent/50 hover:bg-surface-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent">
      <div className="mb-5 flex w-full items-start justify-between gap-3">
        <span className="rounded-xl bg-accent/10 p-3 text-accent"><FiBookOpen aria-hidden="true" size={22} /></span>
        {course.discipline?.trim() && <span className="max-w-[70%] break-words rounded-full border border-border bg-surface-muted px-3 py-1 text-xs font-medium text-text-muted">{course.discipline}</span>}
      </div>
      <h3 className="break-words text-lg font-semibold leading-snug text-text">{course.name}</h3>
      <p className="mt-2 line-clamp-3 break-words text-sm leading-6 text-text-muted">{course.description?.trim() || "No description added yet."}</p>
      <div className="mt-auto w-full pt-6">
        <span className="flex items-center justify-between border-t border-border pt-4 text-sm font-medium text-accent">
          View course
          <FiArrowUpRight aria-hidden="true" size={18} className="transition-transform motion-safe:group-hover:-translate-y-0.5 motion-safe:group-hover:translate-x-0.5" />
        </span>
      </div>
    </button>
  );
}
