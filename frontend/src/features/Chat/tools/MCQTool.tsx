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

export type MultipleChoiceQuestion = MultipleChoiceQuestionBase & {
    topic: string;
    difficulty: DifficultyLevel;
    learning_objective: LearningObjective;
};

export type MultipleChoiceQuestionToolResponse = {
    payload: MultipleChoiceQuestion[];
};


export function parseMultipleChoice(msg: ToolMessage): MultipleChoiceQuestionToolResponse {
    // Eventually add tigher guard railes for this 
    const raw = extractToolPayload(msg) as MultipleChoiceQuestionToolResponse
    return raw
}

function RenderMCQSingle({ question, submitted }: { question: MultipleChoiceQuestion; submitted: boolean }) {
    const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

    const correctIndex = question.options.findIndex((v) => v.correct);
    const selectedIsCorrect = selectedIndex !== null && selectedIndex === correctIndex;

    return (
        <MathJax>
            <article className="rounded-lg border border-border bg-surface p-4 shadow-soft">
                <div className="flex items-start justify-between gap-3">
                    <p className="text-sm font-medium leading-relaxed text-text">{question.question}</p>
                    {submitted ? (
                        <span
                            className={`shrink-0 rounded-full border px-2.5 py-1 text-xs font-semibold ${selectedIsCorrect
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
                        const isSelected = selectedIndex === idx;
                        const isCorrect = idx === correctIndex;
                        const showCorrect = submitted && isCorrect;
                        const showWrong = submitted && isSelected && !isCorrect;

                        return (
                            <button
                                key={`${question.question}-${idx}`}
                                type="button"
                                className={`group w-full rounded-md border px-3 py-2.5 text-left text-sm transition duration-base ease-base ${showCorrect
                                    ? "border-accent-strong bg-surface-muted text-text"
                                    : showWrong
                                        ? "border-border-strong bg-button-secondary text-text"
                                        : isSelected
                                            ? "border-accent bg-surface text-text"
                                            : "border-border bg-surface-strong text-text-muted hover:border-accent/60 hover:text-text"
                                    }`}
                                onClick={() => !submitted && setSelectedIndex(idx)}
                                disabled={submitted}
                            >
                                <span className={`mr-2 inline-block min-w-5 font-semibold ${isSelected ? "text-accent" : "text-text-soft group-hover:text-text-muted"}`}>
                                    {String.fromCharCode(65 + idx)}.
                                </span>
                                {v.option}
                            </button>
                        );
                    })}
                </div>

                {submitted && selectedIndex === null ? (
                    <p className="mt-3 text-xs text-text-muted">
                        Select an option before checking next time.
                    </p>
                ) : null}

                {submitted && !selectedIsCorrect && correctIndex >= 0 ? (
                    <p className="mt-3 rounded-md border border-accent-strong bg-surface-muted px-2.5 py-2 text-xs text-text">
                        Correct answer:{" "}
                        <span className="font-semibold">
                            {String.fromCharCode(65 + correctIndex)}. {question.options[correctIndex]?.option}
                        </span>
                    </p>
                ) : null}
            </article>
        </MathJax>
    );
}


export function RenderMCQ({ payload, onApprove, onCancel, loading, error }: RenderPreviewProps<MultipleChoiceQuestionToolResponse>) {
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false)
    const Qpayload = payload.payload
    if (!Qpayload) {
        return "Loading"
    }

    const handleSubmit = async () => {
        console.log("Submitted")

    }
    return <div className="w-full space-y-3 rounded-xl border border-border bg-surface p-3">
        <h4 className="text-sm font-semibold text-text">Practice Your Understanding</h4>
        {Qpayload.map((v, idx) => <RenderMCQSingle key={`${v.question}-${idx}`} question={v} submitted={isSubmitted}></RenderMCQSingle>)}
        <div>
            <Button onClick={() => setIsSubmitted(prev => !prev)}>
                Check Answers
            </Button>
        </div>


    </div>
}
