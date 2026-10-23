import type { ComponentProps } from "react";
import type { CourseContentType } from "../../../services/courses/types";

const CATEGORIES = [
  { value: "notes", label: "Lecture notes" },
  { value: "lecture", label: "Lecture materials" },
  { value: "exam", label: "Exam" },
  { value: "assignment", label: "Assignment" },
  { value: "quiz", label: "Quiz" },
  { value: "textbook", label: "Textbook" },
  { value: "handout", label: "Handout" },
  { value: "syllabus", label: "Syllabus" },
  { value: "reference", label: "Reference" },
  { value: "other", label: "Other" },
] as const satisfies readonly { value: CourseContentType; label: string; }[];

type Props = Omit<ComponentProps<"select">, "value"> & {
  value: CourseContentType;
};

export function ContentTypeDropDown({ value, className, ...props }: Props) {
  return (
    <select
      {...props}
      value={value}
      className={className ?? "min-w-0 flex-1 rounded-lg border border-border bg-surface px-4 py-3 text-sm text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-60 sm:w-48 sm:flex-none"}
    >
      {CATEGORIES.map(({ value, label }) => (
        <option key={value} value={value}>{label}</option>
      ))}
    </select>
  );
}
