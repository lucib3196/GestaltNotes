import { FiCheckCircle, FiXCircle } from "react-icons/fi";
import Markdown from "../../../../components/Markdown/MarkdownRenderer";
import { secondaryButton } from "../styles";
import type {
  MultipleChoiceSet,
  QuizAction,
  QuizSaveHandler,
  QuizSubmission,
} from "../types";
import QuizFeedback from "./QuizFeedback";

type QuizResultsProps = {
  quiz: MultipleChoiceSet;
  submission: QuizSubmission;
  onReview?: QuizAction;
  onSave?: QuizSaveHandler;
  saveEnabled?: boolean;
  onEdit: () => void;
};

export default function QuizResults({
  quiz,
  submission,
  onReview,
  onSave,
  saveEnabled,
  onEdit,
}: QuizResultsProps) {
  return (
    <div className="space-y-4">
      <div
        role="status"
        className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-border bg-surface-strong p-4"
      >
        <div>
          <h3 className="text-base font-semibold text-text">Your results</h3>
          <p className="mt-1 text-sm text-text-muted">
            {submission.correctCount} of {submission.total} correct ·{" "}
            {Math.round(
              (submission.correctCount / Math.max(submission.total, 1)) * 100,
            )}
            %
          </p>
        </div>
        <button type="button" onClick={onEdit} className={secondaryButton}>
          Edit answers
        </button>
      </div>
      <ol className="space-y-3">
        {submission.results.map((result) => (
          <li
            key={result.questionIndex}
            className="space-y-3 rounded-lg border border-border bg-surface-strong p-4"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span className="text-xs font-medium text-text-soft">
                Question {result.questionIndex + 1}
              </span>
              <span
                className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold ${result.isCorrect ? "bg-accent/10 text-accent" : "bg-surface-muted text-text-muted"}`}
              >
                {result.isCorrect ? (
                  <FiCheckCircle aria-hidden="true" />
                ) : (
                  <FiXCircle aria-hidden="true" />
                )}
                {result.isCorrect === null
                  ? "Unanswered"
                  : result.isCorrect
                    ? "Correct"
                    : "Incorrect"}
              </span>
            </div>
            <div className="text-sm text-text">
              <Markdown>{result.question}</Markdown>
            </div>
            <dl className="space-y-2 text-sm">
              <div>
                <dt className="font-medium text-text-soft">Your answer</dt>
                <dd className="mt-1 text-text">
                  <Markdown>{result.selectedAnswer ?? "Not answered"}</Markdown>
                </dd>
              </div>
              {result.isCorrect !== true && (
                <div>
                  <dt className="font-medium text-text-soft">Correct answer</dt>
                  <dd className="mt-1 text-text">
                    <Markdown>{result.correctAnswer}</Markdown>
                  </dd>
                </div>
              )}
              {result.reasoning && (
                <div>
                  <dt className="font-medium text-text-soft">Your reasoning</dt>
                  <dd className="mt-1 whitespace-pre-wrap break-words text-text-muted">
                    {result.reasoning}
                  </dd>
                </div>
              )}
            </dl>
            <div className="border-t border-border pt-3 text-sm text-text-muted">
              <p className="mb-1 font-medium text-text">Explanation</p>
              <Markdown>{result.explanation}</Markdown>
            </div>
          </li>
        ))}
      </ol>
      <QuizFeedback
        quiz={quiz}
        submission={submission}
        onReview={onReview}
        onSave={onSave}
        saveEnabled={saveEnabled}
      />
    </div>
  );
}
