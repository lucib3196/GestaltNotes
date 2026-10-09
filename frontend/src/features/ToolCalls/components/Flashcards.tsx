import type { FlashcardSet } from "../schemas";

export default function Flashcards({ data }: { data: FlashcardSet }) {
  return (
    <div className="grid gap-3">
      {data.cards.map((card, index) => (
        <details key={index} className="rounded-xl border border-border bg-surface-strong p-4">
          <summary className="cursor-pointer text-sm font-medium text-text">
            {card.front}
          </summary>
          <p className="mt-3 border-t border-border/50 pt-3 text-sm text-text-soft">
            {card.back}
          </p>
        </details>
      ))}
    </div>
  );
}
