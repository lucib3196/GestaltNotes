import type { ReactNode } from "react";
import Markdown from "../../../components/Markdown/MarkdownRenderer";
import type { PageRange, SourceOption } from "../schemas";

export function Equation({ latex }: { latex: string | null }) {
  if (!latex?.trim()) return null;
  return <Markdown>{`$$\n${latex}\n$$`}</Markdown>;
}

export function SourcePages({ reference }: { reference: PageRange | null }) {
  if (!reference) return null;
  const start = reference.start + 1;
  const end = reference.end + 1;
  return (
    <p className="text-xs text-text-muted">
      {start === end ? `Page ${start}` : `Pages ${start}–${end}`}
    </p>
  );
}

export function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="min-w-0 space-y-2">
      <h4 className="text-sm font-semibold text-text">{title}</h4>
      {children}
    </section>
  );
}

export function TextList({ items }: { items: string[] }) {
  if (!items.length) return null;
  return (
    <ul className="list-disc space-y-2 pl-5">
      {items.map((item, index) => <li key={index}><Markdown>{item}</Markdown></li>)}
    </ul>
  );
}

export function ListSection({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null;
  return <Section title={title}><TextList items={items} /></Section>;
}

export function Options({ options }: { options: SourceOption[] }) {
  if (!options.length) return null;
  return (
    <Section title="Options">
      <ul className="space-y-2">
        {options.map((option, index) => (
          <li key={index} className="rounded-md border border-border bg-surface-muted p-3">
            {option.label && <p className="text-xs font-semibold">{option.label}</p>}
            <Markdown>{option.text}</Markdown>
            <p className="mt-1 text-xs text-text-muted">
              {option.is_correct === null ? "Correctness not specified in source"
                : option.is_correct ? "Marked correct in source" : "Marked incorrect in source"}
            </p>
          </li>
        ))}
      </ul>
    </Section>
  );
}
