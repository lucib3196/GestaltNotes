import { useState } from "react";
import type { MultipleChoiceSet } from "../schemas";

export default function MultipleChoiceQuestions({
  data,
}: {
  data: MultipleChoiceSet;
}) {
  const [answers, setAnswers] = useState<Record<number, number>>({});

  return (
    <div className="space-y-3">
      {data.questions.map((question, index) => (
        <fieldset
          key={index}
          className="min-w-0 space-y-3 rounded-xl border border-border bg-surface-strong p-4"
        >
          <legend className="px-1 text-sm font-semibold text-text">
            {index + 1}. {question.question}
          </legend>
          <div className="grid gap-2">
            {question.options.map((option, optionIndex) => (
              <button
                key={optionIndex}
                type="button"
                aria-pressed={answers[index] === optionIndex}
                onClick={() =>
                  setAnswers((previous) => ({
                    ...previous,
                    [index]: optionIndex,
                  }))
                }
                className="rounded-lg border border-border px-3 py-2 text-left text-sm text-text hover:bg-surface-muted aria-pressed:border-accent aria-pressed:bg-accent/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
              >
                {String.fromCharCode(65 + optionIndex)}. {option}
              </button>
            ))}
          </div>
          {answers[index] !== undefined && (
            <div role="status" className="space-y-1 text-sm text-text-soft">
              <p>
                {answers[index] === question.correct_answer_index
                  ? "Correct."
                  : `Correct answer: ${question.options[question.correct_answer_index]}`}
              </p>
              <p>{question.explanation}</p>
            </div>
          )}
        </fieldset>
      ))}
    </div>
  );
}
