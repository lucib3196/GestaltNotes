import type {
  MultipleChoiceQuestionSubmitted,
  MultipleChoiceQuestion,

} from "../api/mcq.types";
import { useMemo, useState } from "react";
import MCQCard from "./MCQCard";
import MCQOption from "./MCQOptions";
import MCQHeader from "./MCQHeader";
import MCQFeedback from "./MCQFeedback";


type MCQSingleProps = {
  question: MultipleChoiceQuestion;
  submitted?: boolean;
  selectedIndex?: number | null;
  onSelectedIndexChange?: (next: number) => void;
};

export default function RenderMCQSingle({
  question,
  submitted = false,
  selectedIndex,
  onSelectedIndexChange,
}: MCQSingleProps) {
  const [internalSelectedIndex, setInternalSelectedIndex] = useState<
    number | null
  >(null);
  const isSelectedControlled = selectedIndex !== undefined;
  const resolvedSelectedIndex = isSelectedControlled
    ? selectedIndex
    : internalSelectedIndex;

  // Extract index of correct answer
  const correctIndex = question.options.findIndex((v) => v.correct);
  const isCorrect = resolvedSelectedIndex === correctIndex;

  const handleSelect = (idx: number) => {
    if (!isSelectedControlled) setInternalSelectedIndex(idx);
    onSelectedIndexChange?.(idx);
  };

  return (
    <MCQCard>
      <MCQHeader
        question={question}
        isCorrect={isCorrect}
        submitted={submitted}
      />
      {/* Render the actual options */}
      <div className="mt-3 space-y-2">
        {question.options.map((v, idx) => {
          return (
            <MCQOption
              v={v}
              idx={idx}
              isCorrect={idx === correctIndex}
              setSelected={handleSelect}
              isSelected={idx === resolvedSelectedIndex}
              submitted={submitted}
            />
          );
        })}
      </div>
      {/* Feedback Sections */}
      <MCQFeedback
        question={question}
        isCorrect={isCorrect}
        submitted={submitted}
        selected={resolvedSelectedIndex ?? null}
        correctIndex={correctIndex}
      />
    </MCQCard>
  );
}

type MCQListProps = {
  questions: MultipleChoiceQuestion[];
  onSubmitBatch?: (submissions: MultipleChoiceQuestionSubmitted[]) => void;
  onQuestionSubmit?: (
    questionIndex: number,
    submission: MultipleChoiceQuestionSubmitted,
  ) => void;
  submitLabel?: string;
  resetLabel?: string;
};

export function RenderMCQList({
  questions,
  onSubmitBatch,
  onQuestionSubmit,
  submitLabel = "Submit",
  resetLabel = "Reset",
}: MCQListProps) {
  const [submitted, setSubmitted] = useState(false);
  const [selectedByQuestion, setSelectedByQuestion] = useState<
    Record<number, number | null>
  >({});

  const answeredCount = useMemo(
    () => questions.filter((_, idx) => selectedByQuestion[idx] != null).length,
    [questions, selectedByQuestion],
  );

  const allAnswered =
    questions.length > 0 && answeredCount === questions.length;

  const handleSelect = (questionIndex: number, selected: number) => {
    if (submitted) return;
    setSelectedByQuestion((prev) => ({ ...prev, [questionIndex]: selected }));
  };

  const buildSubmission = (
    question: MultipleChoiceQuestion,
    selected: number,
  ): MultipleChoiceQuestionSubmitted => {
    const correctIndex = question.options.findIndex((opt) => opt.correct);
    return {
      ...question,
      submission: {
        selected: question.options[selected].option,
        is_correct: selected === correctIndex,
      },
    };
  };

  const handleSubmit = () => {
    if (!allAnswered) return;

    const batch = questions.map((question, idx) =>
      buildSubmission(question, selectedByQuestion[idx] as number),
    );

    setSubmitted(true);
    onSubmitBatch?.(batch);
    batch.forEach((submission, idx) => onQuestionSubmit?.(idx, submission));
  };

  const handleReset = () => {
    setSubmitted(false);
    setSelectedByQuestion({});
  };

  return (
    <div className="space-y-4">
      {questions.map((question, idx) => (
        <RenderMCQSingle
          key={`${question.question}-${idx}`}
          question={question}
          submitted={submitted}
          selectedIndex={selectedByQuestion[idx] ?? null}
          onSelectedIndexChange={(selected) => handleSelect(idx, selected)}
        />
      ))}
      <div className="mt-3 flex items-center gap-2">
        <button
          type="button"
          className="rounded-md border border-accent bg-surface px-3 py-2 text-sm font-medium text-text transition duration-base ease-base hover:border-accent/70 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={submitted || !allAnswered}
          onClick={handleSubmit}
        >
          {submitLabel}
        </button>
        <button
          type="button"
          className="rounded-md border border-accent bg-surface px-3 py-2 text-sm font-medium text-text transition duration-base ease-base hover:border-accent/70 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={!submitted}
          onClick={handleReset}
        >
          {resetLabel}
        </button>
      </div>
    </div>
  );
}
