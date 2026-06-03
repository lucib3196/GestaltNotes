import type { ConceptualQuestion as ConceptualQuestionType } from "../../models/lecture.types";
import BaseLectureEntry from "./BaseLectureEntry";

type ConceptualQuestionProps = {
  question: ConceptualQuestionType;
};

export default function ConceptualQuestion({
  question,
}: ConceptualQuestionProps) {
  return (
    <BaseLectureEntry
      eyebrow="Conceptual question"
      title={question.question}
      reference={question.reference}
      tags={question.topics}
    >
      <ul className="space-y-2">
        {question.options.map((option) => (
          <li
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
          </li>
        ))}
      </ul>

      <p className="leading-relaxed text-text-muted">{question.explanation}</p>
    </BaseLectureEntry>
  );
}
