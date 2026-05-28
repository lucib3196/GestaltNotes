import type { ToolMessage } from "langchain";
import type { RenderPreviewProps } from "./types";
import { extractToolPayload } from "../utils";
import { MathJax } from "better-react-mathjax";
import { Button } from "../../../components/Button";
import { useState } from "react";
export type DifficultyLevel = string;
export type LearningObjective = string;

export type Option = {
  option: string;
  correct: boolean;
};

export type MultipleChoiceQuestionBase = {
  question: string;
  options: Option[];
};
type MCQSubmission = {
  qid: number;
  selected: string;
  is_correct: boolean;
};
export type MultipleChoiceQuestion = MultipleChoiceQuestionBase & {
  topic: string;
  difficulty: DifficultyLevel;
  learning_objective: LearningObjective;
};

export type MultipleChoiceQuestionToolResponse = {
  payload: MultipleChoiceQuestion[];
};

export function parseMultipleChoice(
  msg: ToolMessage,
): MultipleChoiceQuestionToolResponse {
  // Eventually add tigher guard railes for this
  const raw = extractToolPayload(msg) as MultipleChoiceQuestionToolResponse;
  return raw;
}

function RenderMCQSingle({
  question,
  questionIndex,
  submitted,
  selectedAnswer,
  onSelectAnswer,
}: {
  question: MultipleChoiceQuestion;
  questionIndex: number;
  submitted: boolean;
  selectedAnswer?: MCQSubmission;
  onSelectAnswer: (answer: MCQSubmission, optionIndex: number) => void;
}) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const correctIndex = question.options.findIndex((v) => v.correct);

  const effectiveSelectedIndex =
    submitted && selectedAnswer
      ? question.options.findIndex((v) => v.option === selectedAnswer.selected)
      : selectedIndex;

  const selectedIsCorrect =
    submitted && selectedAnswer
      ? selectedAnswer.is_correct
      : effectiveSelectedIndex !== null &&
        effectiveSelectedIndex === correctIndex;

  const handleClick = (
    option: Option,
    optionIndex: number,
    isCorrect: boolean,
  ) => {
    if (submitted) return;
    setSelectedIndex(optionIndex);
    onSelectAnswer(
      {
        qid: questionIndex,
        selected: option.option,
        is_correct: isCorrect,
      },
      optionIndex,
    );
  };

  return (
    <MathJax>
      <article className="rounded-lg border border-border bg-surface p-4 shadow-soft">
        {/* Question View */}
        <div className="flex items-start justify-between gap-3">
          <p className="text-sm font-medium leading-relaxed text-text">
            {question.question}
          </p>
          {submitted ? (
            <span
              className={`shrink-0 rounded-full border px-2.5 py-1 text-xs font-semibold ${
                selectedIsCorrect
                  ? "border-accent-strong bg-surface-muted text-text"
                  : "border-border-strong bg-button-secondary text-text-muted"
              }`}
            >
              {selectedIsCorrect ? "Correct" : "Incorrect"}
            </span>
          ) : null}
        </div>

        <div className="mt-3 space-y-2">
          {question.options.map((v, idx) => {
            const isSelected = effectiveSelectedIndex === idx;
            const isCorrect = idx === correctIndex;
            const showCorrect = submitted && isCorrect;
            const showWrong = submitted && isSelected && !isCorrect;

            return (
              <button
                key={`${idx}`}
                type="button"
                className={`group w-full rounded-md border px-3 py-2.5 text-left text-sm transition duration-base ease-base ${
                  showCorrect
                    ? "border-accent-strong bg-surface-muted text-text"
                    : showWrong
                      ? "border-border-strong bg-button-secondary text-text"
                      : isSelected
                        ? "border-accent bg-surface text-text"
                        : "border-border bg-surface-strong text-text-muted hover:border-accent/60 hover:text-text"
                }`}
                onClick={() => handleClick(v, idx, isCorrect)}
                disabled={submitted}
              >
                <span
                  className={`mr-2 inline-block min-w-5 font-semibold ${isSelected ? "text-accent" : "text-text-soft group-hover:text-text-muted"}`}
                >
                  {String.fromCharCode(65 + idx)}.
                </span>
                {v.option}
              </button>
            );
          })}
        </div>

        {/* Feedback Sections */}

        {submitted && effectiveSelectedIndex === null ? (
          <p className="mt-3 text-xs text-text-muted">
            Select an option before checking next time.
          </p>
        ) : null}

        {submitted && !selectedIsCorrect && correctIndex >= 0 ? (
          <p className="mt-3 rounded-md border border-accent-strong bg-surface-muted px-2.5 py-2 text-xs text-text">
            Correct answer:{" "}
            <span className="font-semibold">
              {String.fromCharCode(65 + correctIndex)}.{" "}
              {question.options[correctIndex]?.option}
            </span>
          </p>
        ) : null}
      </article>
    </MathJax>
  );
}

export function RenderMCQ({
  payload,
  onApprove,
  onCancel,
  loading,
  error,
}: RenderPreviewProps<MultipleChoiceQuestionToolResponse>) {
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [answersByQuestion, setAnswersByQuestion] = useState<
    Record<number, MCQSubmission>
  >({});
  const Qpayload = payload.payload;

  if (!Qpayload) {
    return "Loading";
  }

  const handleSelectAnswer = (answer: MCQSubmission) => {
    setAnswersByQuestion((prev) => ({
      ...prev,
      [answer.qid]: answer,
    }));
  };

  const handleSubmit = async () => {
    setIsSubmitted(true);
    const payloadWithAnswers = {
      ...payload,
      payload: Qpayload.map((q, idx) => ({
        ...q,
        user_submission: answersByQuestion[idx] ?? null,
      })),
    };
    console.log("Sending payload", payloadWithAnswers);
    onApprove?.(payloadWithAnswers);
  };

  return (
    <div className="w-full space-y-3 rounded-xl border border-border bg-surface p-3">
      <h4 className="text-sm font-semibold text-text">
        Practice Your Understanding
      </h4>
      {Qpayload.map((v, idx) => (
        <RenderMCQSingle
          key={`${v.question}-${idx}`}
          question={v}
          questionIndex={idx}
          submitted={isSubmitted}
          selectedAnswer={answersByQuestion[idx]}
          onSelectAnswer={handleSelectAnswer}
        />
      ))}
      <div>
        <Button onClick={handleSubmit}>Check Answers</Button>
      </div>
    </div>
  );
}
