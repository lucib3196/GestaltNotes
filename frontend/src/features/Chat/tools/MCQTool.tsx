import type { ToolMessage } from "langchain";
import type { RenderPreviewProps } from "./types";
import { extractToolPayload } from "../utils";
import { MathJax } from "better-react-mathjax";
import { Button } from "../../../components/Button";
export type DifficultyLevel = string;
export type LearningObjective = string;

export type Option = {
    option: string;
    is_correct: boolean;
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


function RenderMCQSingle({ question }: { question: MultipleChoiceQuestion }) {
    return (
        <MathJax>
            <article className="rounded-lg border border-border bg-surface p-3">
                <p className="text-sm font-medium text-text">{question.question}</p>
                <div className="mt-2 space-y-2">
                    {question.options.map((v, idx) => (
                        <div
                            key={`${question.question}-${idx}`}
                            className="rounded-md border border-border bg-surface-strong px-3 py-2 text-sm text-text-muted"
                        >
                            <span className="mr-2 text-text-soft">{String.fromCharCode(65 + idx)}.</span>
                            {v.option}
                        </div>
                    ))}
                </div>
            </article>
        </MathJax>
    );
}


export function RenderMCQ({ payload }: RenderPreviewProps<MultipleChoiceQuestionToolResponse>) {
    const Qpayload = payload.payload
    if (!Qpayload) {
        return "Loading"
    }
    return <div className="w-full space-y-3 rounded-xl border border-border bg-surface p-3">
        <h4 className="text-sm font-semibold text-text">Practice Your Understanding</h4>
        {Qpayload.map((v, idx) => <RenderMCQSingle key={`${v.question}-${idx}`} question={v}></RenderMCQSingle>)}
        <div>
            <Button>
                Check Answers
            </Button>
        </div>


    </div>
}
