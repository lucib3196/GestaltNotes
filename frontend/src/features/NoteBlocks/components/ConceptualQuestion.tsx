import Markdown from "../../../components/Markdown/MarkdownRenderer";
import type { ConceptualQuestionContent } from "../schemas";
import { ListSection, Options, Section, SourcePages } from "./shared";

export default function ConceptualQuestion({ content }: { content: ConceptualQuestionContent }) {
  return (
    <div className="space-y-4">
      <Markdown>{content.question}</Markdown>
      <ListSection title="Topics" items={content.topics} />
      <Options options={content.options} />
      {content.answer !== null && (
        <Section title="Answer"><Markdown>{content.answer}</Markdown></Section>
      )}
      {content.explanation !== null && (
        <Section title="Explanation"><Markdown>{content.explanation}</Markdown></Section>
      )}
      <SourcePages reference={content.reference} />
    </div>
  );
}
