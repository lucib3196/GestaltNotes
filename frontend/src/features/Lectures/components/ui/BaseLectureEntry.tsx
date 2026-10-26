import type { ReactNode } from "react";
import type { PageRange } from "../../models/lecture.types";
import Markdown from "../../../../components/Markdown/MarkdownRenderer";

type BaseLectureEntryVariant = "bordered" | "borderless";

type BaseLectureEntryProps = {
  title: string;
  eyebrow?: string;
  subtitle?: string;
  reference?: PageRange | null;
  tags?: string[];
  variant?: BaseLectureEntryVariant;
  children?: ReactNode;
};

export default function BaseLectureEntry({
  title,
  eyebrow,
  subtitle,
  reference,
  tags = [],
  variant = "bordered",
  children,
}: BaseLectureEntryProps) {
  const cardClassName =
    variant === "bordered"
      ? "rounded-lg border border-border bg-surface p-4 text-text"
      : "rounded-lg bg-surface p-4 text-text";

  return (
    <article className={cardClassName}>
      <div className="flex flex-col gap-2">
        {eyebrow && (
          <p className="text-xs font-semibold uppercase text-accent">
            {eyebrow}
          </p>
        )}

        <div className="flex flex-col gap-1">
          <h3 className="text-base font-semibold leading-snug"><Markdown>{title}</Markdown></h3>
          {subtitle && <div className="text-sm text-text-muted"><Markdown>{subtitle}</Markdown></div>}
        </div>

        {(tags.length > 0 || reference) && (
          <div className="flex flex-wrap items-center gap-2">
            {tags.map((tag) => (
              <div
                key={tag}
                className="rounded-md border border-border bg-surface-muted px-2 py-1 text-xs text-text-muted"
              >
                <Markdown>{tag}</Markdown>
              </div>
            ))}

            {reference && (
              <span className="rounded-md border border-border bg-surface-muted px-2 py-1 text-xs text-text-muted">
                Pages {reference.start_page}-{reference.end_page}
              </span>
            )}
          </div>
        )}

        {children && <div className="mt-2 space-y-3 text-sm">{children}</div>}
      </div>
    </article>
  );
}
