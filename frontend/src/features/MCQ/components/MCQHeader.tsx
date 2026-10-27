import type { MultipleChoiceQuestion } from "../api/mcq.types";
import Markdown from "../../../components/Markdown/MarkdownRenderer";

type MCQHeaderProps = {
    question: MultipleChoiceQuestion;
    submitted: boolean;
    isCorrect: boolean;
};

export default function MCQHeader({
    question,
    submitted,
    isCorrect,
}: MCQHeaderProps) {
    return (
            <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 text-sm font-medium leading-relaxed text-text">
                    <Markdown>{question.question}</Markdown>
                </div>
                {submitted ? (
                    <span
                        className={`shrink-0 rounded-full border px-2.5 py-1 text-xs font-semibold ${isCorrect
                            ? "border-accent-strong bg-surface-muted text-text"
                            : "border-border-strong bg-button-secondary text-text-muted"
                            }`}
                    >
                        {isCorrect ? "Correct" : "Incorrect"}
                    </span>
                ) : null}
            </div>
    );
}