import { useId } from "react";
import Markdown from "../../../../components/Markdown/MarkdownRenderer";
import type { MCQQuestion } from "../types";
import { useState } from "react";
type QuestionCardProps = {
  index: number;
  question: MCQQuestion;
  selectedOption?: number;
  reasoning: string;
  onAnswerChange: (optionIndex: number) => void;
  onReasoningChange: (reasoning: string) => void;
};

export default function QuestionCard({
  index,
  question,
  selectedOption,
  reasoning,
  onAnswerChange,
  onReasoningChange,
}: QuestionCardProps) {
  const id = useId();
  const [show, setShow] = useState<boolean>(false)
  return (
    <div className="space-y-4">
      <fieldset className="min-w-0 space-y-4 rounded-lg border border-border bg-surface-strong p-4 sm:p-5">
        <legend className="px-1 text-xs font-semibold uppercase tracking-wider text-text-soft">
          Question {index + 1}
        </legend>
        <div className="text-sm font-medium text-text">
          <Markdown>{question.question}</Markdown>
        </div>
        <div className="grid gap-2">
          {question.options.map((option, optionIndex) => (
            <label
              key={optionIndex}
              className={`flex cursor-pointer items-start gap-3 rounded-md border px-3 py-3 text-sm text-text transition-colors focus-within:ring-2 focus-within:ring-accent/60 ${selectedOption === optionIndex ? "border-accent bg-accent/10" : "border-border hover:bg-surface-muted"}`}
            >
              <input
                type="radio"
                name={`${id}-answer`}
                checked={selectedOption === optionIndex}
                onChange={() => onAnswerChange(optionIndex)}
                className="mt-1 h-4 w-4 shrink-0 accent-accent"
              />
              <span className="min-w-0 flex-1">
                <span className="mr-2 font-semibold">
                  {String.fromCharCode(65 + optionIndex)}.
                </span>
                {option}
              </span>
            </label>
          ))}
        </div>
      </fieldset>
      <button className="" onClick={()=>setShow((prev)=>!prev)}>Add Context </button>

      {show && <div className="space-y-2">
        <label
          htmlFor={`${id}-reasoning`}
          className="block text-sm font-medium text-text"
        >
          Why did you choose this answer?{" "}
          <span className="font-normal text-text-soft">(optional)</span>
        </label>
        <textarea
          id={`${id}-reasoning`}
          rows={3}
          value={reasoning}
          onChange={(event) => onReasoningChange(event.target.value)}
          placeholder="Share your reasoning, calculation, or what made you unsure…"
          aria-describedby={`${id}-hint`}
          className="block min-h-24 w-full resize-y rounded-md border border-border bg-surface-strong px-3 py-2.5 text-sm leading-relaxed text-text outline-none placeholder:text-text-soft focus:border-accent focus:ring-2 focus:ring-accent/20"
        />
        <p id={`${id}-hint`} className="text-xs text-text-soft">
          Your reasoning can help the AI give more specific feedback if you
          request a review.
        </p>
      </div>}
    </div>
  );
}
