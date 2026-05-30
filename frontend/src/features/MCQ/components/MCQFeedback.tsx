import type { MultipleChoiceQuestion } from "../api/mcq.types";

type MCQFeedbackProps = {
    question: MultipleChoiceQuestion;
    selected: number | null;
    correctIndex: number;
    submitted: boolean;
    isCorrect: boolean;
};

export default  function MCQFeedback({
    question,
    submitted,
    isCorrect,
    selected,
    correctIndex,
}: MCQFeedbackProps) {
    return (
        <>
            {submitted && selected === null ? (
                <p className="mt-3 text-xs text-text-muted">
                    Select an option before checking next time.
                </p>
            ) : null}
            {submitted && !isCorrect && correctIndex >= 0 ? (
                <p className="mt-3 rounded-md border border-accent-strong bg-surface-muted px-2.5 py-2 text-xs text-text">
                    Correct answer:{" "}
                    <span className="font-semibold">
                        {String.fromCharCode(65 + correctIndex)}.{" "}
                        {question.options[correctIndex]?.option}
                    </span>
                </p>
            ) : null}
        </>
    );
}