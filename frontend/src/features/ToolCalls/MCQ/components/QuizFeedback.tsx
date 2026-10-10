import { useRef, useState } from "react";
import { FiSave, FiZap } from "react-icons/fi";
import { primaryButton, secondaryButton } from "../styles";
import type { MultipleChoiceSet, QuizAction, QuizSaveHandler, QuizSubmission } from "../types";

type QuizFeedbackProps = {
  quiz: MultipleChoiceSet;
  submission: QuizSubmission;
  onReview?: QuizAction;
  onSave?: QuizSaveHandler;
  saveEnabled?: boolean;
};

export default function QuizFeedback({ quiz, submission, onReview, onSave, saveEnabled = false }: QuizFeedbackProps) {
  const [action, setAction] = useState<"review" | "save" | null>(null);
  const [reviewRequested, setReviewRequested] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pending = useRef(false);
  async function runAction(kind: "review" | "save") {
    if (pending.current) return;
    if (kind === "review" && (!onReview || reviewRequested)) return;
    if (kind === "save" && (!saveEnabled || !onSave || saved)) return;
    pending.current = true;
    setAction(kind);
    setError(null);
    try {
      if (kind === "review") {
        await onReview?.(submission);
        setReviewRequested(true);
      } else {
        await onSave?.({ quiz, submission });
        setSaved(true);
      }
    } catch {
      setError(kind === "review" ? "Could not request an AI review. Please try again." : "Could not save this quiz. Please try again.");
    } finally {
      pending.current = false;
      setAction(null);
    }
  }
  return (
    <section aria-label="Quiz feedback" className="space-y-3 rounded-lg border border-accent/20 bg-accent/5 p-4">
      <div className="space-y-1">
        <h3 className="text-sm font-semibold text-text">Understand your results</h3>
        <p className="text-sm leading-relaxed text-text-muted">Ask AI to review your answers and reasoning, identify concepts you may be struggling with, and suggest what to practice next.</p>
      </div>
      <div className="flex flex-wrap gap-2">
        <button type="button" disabled={!onReview || action !== null || reviewRequested} onClick={() => void runAction("review")} className={primaryButton}><FiZap aria-hidden="true" />{action === "review" ? "Requesting review…" : reviewRequested ? "AI review requested" : "Review my answers with AI"}</button>
        <button type="button" disabled={!saveEnabled || !onSave || action !== null || saved} onClick={() => void runAction("save")} title={!saveEnabled ? "Saving quizzes will be available soon" : undefined} className={secondaryButton}><FiSave aria-hidden="true" />{action === "save" ? "Saving…" : saved ? "Quiz saved" : "Save quiz"}</button>
      </div>
      {!saveEnabled && <p className="text-xs text-text-soft">Saving quizzes will be available soon.</p>}
      {reviewRequested && <p role="status" className="text-xs text-text-muted">Your review was requested. Feedback will appear in the chat.</p>}
      {error && <p role="alert" className="text-sm text-red-500">{error}</p>}
    </section>
  );
}
