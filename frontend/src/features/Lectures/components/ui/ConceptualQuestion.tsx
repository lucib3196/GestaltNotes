import type { ConceptualQuestion as ConceptualQuestionType } from "../../models/lecture.types";
import { RenderMCQSingle } from "../../../MCQ";
import BaseLectureEntry from "./BaseLectureEntry";
import type { ConceptualQuestion } from "../../models/lecture.types";
import type { MultipleChoiceQuestion, Option } from "../../../MCQ";
import { useMemo } from "react";
import { useState } from "react";
function toMCQ(val: ConceptualQuestion): MultipleChoiceQuestion {
  const cleanedOptions: Option[] = val.options.map((opt) => ({
    correct: opt.is_correct,
    option: opt.text,
  }));
  return {
    question: val.question,
    options: cleanedOptions,
    topic: val.topics.join(", "),
    difficulty: "medium",
    learning_objective: "",
  };
}

type ConceptualQuestionProps = {
  question: ConceptualQuestionType;
};

export default function ConceptualQuestion({
  question,
}: ConceptualQuestionProps) {
  const [submitted, setIsSubmitted] = useState<boolean>(false)
  const normalized = useMemo(() => toMCQ(question), [question])

  const handleSubmit = () => {
    setIsSubmitted(true)
  }
  const handleReset = () => {
    setIsSubmitted(false);
  }

  return (
    <BaseLectureEntry
      eyebrow="Conceptual question"
      title={""}
      reference={question.reference}
      tags={question.topics}
      variant="borderless"
    >
      <div className="space-y-4">
        <ul className="space-y-2">
          <RenderMCQSingle question={normalized} submitted={submitted} />
        </ul>

        <div className="flex flex-col-reverse gap-2 border-t border-border/60 pt-4 sm:flex-row sm:items-center sm:justify-end">
          <button
            type="button"
            className="inline-flex min-h-10 items-center justify-center rounded-md border border-border bg-button-secondary px-4 py-2 text-sm font-medium text-text transition duration-base ease-base hover:border-border-strong hover:bg-surface-muted hover:text-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/35 disabled:cursor-not-allowed disabled:opacity-50"
            disabled={!submitted}
            onClick={handleReset}
          >
            Reset
          </button>
          <button
            type="button"
            className="inline-flex min-h-10 items-center justify-center rounded-md border border-accent bg-accent px-4 py-2 text-sm font-semibold text-bg transition duration-base ease-base hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/45 disabled:cursor-not-allowed disabled:opacity-50"
            disabled={submitted}
            onClick={handleSubmit}
          >
            Submit
          </button>
        </div>
      </div>

      {submitted && (
        <p className="rounded-md border border-accent/25 bg-accent/10 px-4 py-3 leading-relaxed text-text">
          {question.explanation}
        </p>
      )}
    </BaseLectureEntry>
  );
}
