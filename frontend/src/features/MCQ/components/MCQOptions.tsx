import type { Option } from "../api/mcq.types";

type MCQOptionProps = {
    v: Option;
    idx: number;
    isSelected: boolean;
    setSelected: (idx: number) => void;
    submitted: boolean;
    isCorrect: boolean;
};

export default function MCQOption({
    v,
    idx,
    submitted,
    isSelected,
    isCorrect,
    setSelected,
}: MCQOptionProps) {

    const showCorrect = submitted && isCorrect;
    const showWrong = submitted && isSelected && !isCorrect;
    const selectedStateClass = showCorrect
        ? "border-accent-strong bg-surface-muted text-text"
        : showWrong
            ? "border-red-500 bg-button-secondary text-text"
            : isSelected
                ? "border-accent bg-surface text-text"
                : "border-border bg-surface-strong text-text-muted hover:border-accent/60 hover:text-text";
    return (
        <button
            key={`${idx}`}
            type="button"
            className={`group w-full rounded-md border px-3 py-2.5 text-left text-sm transition duration-base ease-base ${selectedStateClass}`}
            onClick={() => setSelected(idx)}
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
}