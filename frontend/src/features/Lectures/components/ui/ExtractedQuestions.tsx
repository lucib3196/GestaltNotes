import type { ExtractedQuestion } from "../../models/lecture.types";
import BaseLectureEntry from "./BaseLectureEntry";
import Markdown from "../../../Chat/components/MardownRender";
type ExtractedQuestionsProps = {
  question: ExtractedQuestion;
};

export default function ExtractedQuestions({
  question,
}: ExtractedQuestionsProps) {


  const formatted = question.solution.join("\n\n").replace(/\r\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();

  return (
    <BaseLectureEntry
      eyebrow="Extracted question"
      title={question.question_text}
      subtitle={question.qtype}
      reference={question.reference}
      tags={question.topics}
    >
      {question.options && question.options.length > 0 && (
        <ul className="space-y-2">
          {question.options.map((option) => (
            <ul
              key={option.text}
              className="rounded-md border border-border bg-surface-muted px-3 py-2 text-text-muted"
            >
              <span
                className={
                  option.is_correct ? "font-semibold text-accent-strong" : ""
                }
              >
                {option.text}
              </span>
            </ul>
          ))}
        </ul>
      )}

      {question.solution.length > 0 && (
        <div>
          <Markdown>{formatted}</Markdown>
        </div>
      )}
    </BaseLectureEntry>
  );
}
