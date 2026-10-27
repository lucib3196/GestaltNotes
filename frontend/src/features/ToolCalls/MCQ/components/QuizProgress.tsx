export default function QuizProgress({ index, answered, total }: { index: number; answered: number; total: number }) {
  return (
    <div className="space-y-2">
      <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
        <span aria-live="polite" className="font-medium text-text">Question {index + 1} of {total}</span>
        <span className="text-text-muted">{answered} of {total} answered</span>
      </div>
      <progress value={answered} max={total} aria-label="Quiz completion" aria-valuetext={`${answered} of ${total} questions answered`} className="block h-2 w-full overflow-hidden rounded-full border-0 bg-surface-muted [&::-webkit-progress-bar]:rounded-full [&::-webkit-progress-bar]:bg-surface-muted [&::-webkit-progress-value]:rounded-full [&::-webkit-progress-value]:bg-accent [&::-moz-progress-bar]:rounded-full [&::-moz-progress-bar]:bg-accent" />
    </div>
  );
}
