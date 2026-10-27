import Markdown from "../../../components/Markdown/MarkdownRenderer";
import type { LectureSummaryContent } from "../schemas";
import { ListSection } from "./shared";

export default function LectureSummary({ content }: { content: LectureSummaryContent }) {
  return (
    <div className="space-y-4">
      <div className="text-base font-semibold"><Markdown>{content.title}</Markdown></div>
      <p className="text-xs text-text-muted">Teaching emphasis: {content.kind}</p>
      <Markdown>{content.summary}</Markdown>
      <ListSection title="Topics" items={content.topics} />
      <ListSection title="Learning objectives" items={content.objectives} />
      <ListSection title="Prerequisites" items={content.prerequisites} />
    </div>
  );
}
