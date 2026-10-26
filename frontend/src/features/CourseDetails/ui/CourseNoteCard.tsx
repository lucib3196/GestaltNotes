import type { ReactNode } from "react";

export function CourseNoteCard({
  selected = false,
  children,
}: {
  selected?: boolean;
  children: ReactNode;
}) {
  return (
    <div
      className={`rounded-xl p-3 transition-colors ${
        selected ? "bg-accent/10" : "hover:bg-surface-muted"
      }`}
    >
      {children}
    </div>
  );
}
