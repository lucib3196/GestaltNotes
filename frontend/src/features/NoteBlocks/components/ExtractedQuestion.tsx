import Markdown from "../../../components/Markdown/MarkdownRenderer";
import type { ExtractedQuestionContent } from "../schemas";
import { Equation, ListSection, Options, Section, SourcePages } from "./shared";

export default function ExtractedQuestion({ content }: { content: ExtractedQuestionContent }) {
  return (
    <div className="space-y-4">
      <p className="text-xs text-text-muted">Category: {content.kind.replaceAll("_", " ")}</p>
      <Markdown>{content.question}</Markdown>
      <ListSection title="Topics" items={content.topics} />
      <Options options={content.options} />
      {content.solution.length > 0 ? (
        <Section title="Source solution">
          <ol className="list-decimal space-y-4 pl-5">
            {content.solution.map((step, index) => (
              <li key={index} className="min-w-0 space-y-2">
                <Markdown>{step.explanation}</Markdown>
                <Equation latex={step.equation} />
                <SourcePages reference={step.reference} />
              </li>
            ))}
          </ol>
        </Section>
      ) : <p className="text-sm text-text-muted">No solution steps provided in the source.</p>}
      {content.answer !== null && (
        <Section title="Source answer"><Markdown>{content.answer}</Markdown></Section>
      )}
      <ListSection title="Missing or unclear information" items={content.gaps} />
      <SourcePages reference={content.reference} />
    </div>
  );
}
