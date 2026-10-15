import { useRef, useState } from "react";
import { FiCheckCircle } from "react-icons/fi";
import QuestionCard from "./components/QuestionCard";
import QuizProgress from "./components/QuizProgress";
import QuizResults from "./components/QuizResults";
import { primaryButton, secondaryButton } from "./styles";
import type { AnswerMap, MultipleChoiceSet, QuizAction, QuizSaveHandler, QuizSubmission, ReasoningMap } from "./types";
import { buildQuizSubmission } from "./utils";

export type MultipleChoiceQuizProps = {
  data: MultipleChoiceSet;
  onSubmit?: QuizAction;
  onReview?: QuizAction;
  onSave?: QuizSaveHandler;
  saveEnabled?: boolean;
};

export default function MultipleChoiceQuiz({ data, onSubmit, onReview, onSave, saveEnabled = false }: MultipleChoiceQuizProps) {
  const [answers, setAnswers] = useState<AnswerMap>({});
  const [reasoning, setReasoning] = useState<ReasoningMap>({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const [submission, setSubmission] = useState<QuizSubmission | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pending = useRef(false);
  const total = data.questions.length;
  const questionIndex = Math.min(currentIndex, Math.max(0, total - 1));
  const question = data.questions[questionIndex];
  const answeredCount = data.questions.filter((_, index) => answers[index] !== undefined).length;
  const complete = total > 0 && answeredCount === total;

  async function submitAnswers() {
    if (!complete || pending.current) return;
    pending.current = true;
    setSubmitting(true);
    setError(null);
    const next = buildQuizSubmission(data, answers, reasoning);
    try {
      await onSubmit?.(next);
      setSubmission(next);
    } catch {
      setError("Could not submit your answers. Please try again.");
    } finally {
      pending.current = false;
      setSubmitting(false);
    }
  }

  if (!question) return <p className="text-sm text-text-muted">No questions available.</p>;
  return (
    <section aria-label={data.quiz_title ?? "Practice quiz"} className="w-full min-w-0 space-y-4 rounded-lg border border-border bg-surface p-4 sm:p-5">
      <header className="space-y-1"><h2 className="text-base font-semibold text-text">{data.quiz_title ?? "Practice quiz"}</h2>{data.description && <p className="text-sm leading-relaxed text-text-muted">{data.description}</p>}</header>
      {submission ? (
        <QuizResults quiz={data} submission={submission} onReview={onReview} onSave={onSave} saveEnabled={saveEnabled} onEdit={() => setSubmission(null)} />
      ) : (
        <>
          <QuizProgress index={questionIndex} answered={answeredCount} total={total} />
          <fieldset disabled={submitting} className="min-w-0 space-y-4">
            <QuestionCard key={questionIndex} index={questionIndex} question={question} selectedOption={answers[questionIndex]} reasoning={reasoning[questionIndex] ?? ""} onAnswerChange={(option) => setAnswers((previous) => ({ ...previous, [questionIndex]: option }))} onReasoningChange={(text) => setReasoning((previous) => ({ ...previous, [questionIndex]: text }))} />
            <div className="flex items-center justify-between gap-3 border-t border-border pt-3">
              <button type="button" disabled={questionIndex === 0} onClick={() => setCurrentIndex(questionIndex - 1)} className={secondaryButton}>Previous</button>
              <button type="button" disabled={questionIndex === total - 1} onClick={() => setCurrentIndex(questionIndex + 1)} className={secondaryButton}>Next</button>
            </div>
          </fieldset>
          <div className="flex flex-wrap items-center justify-between gap-3 rounded-md bg-surface-muted p-3">
            <p className="text-xs text-text-muted">{complete ? "Ready to check your answers. AI review is optional after submission." : `Answer ${total - answeredCount} more ${total - answeredCount === 1 ? "question" : "questions"} to submit. `}</p>
            <button type="button" disabled={!complete || submitting} onClick={() => void submitAnswers()} className={`${primaryButton} w-full sm:w-auto`}><FiCheckCircle aria-hidden="true" />{submitting ? "Submitting…" : "Submit answers"}</button>
          </div>
          {error && <p role="alert" className="text-sm text-red-500">{error}</p>}
        </>
      )}
    </section>
  );
}
