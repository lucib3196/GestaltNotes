import { useId, useState } from "react";
import { motion, useReducedMotion } from "motion/react";
import { MathJax } from "better-react-mathjax";
import type { FlashcardSet } from "../schemas/practice";

const buttonClass =
  "rounded-md border border-border bg-surface px-3 py-2 text-sm text-text transition-colors hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 disabled:cursor-not-allowed disabled:opacity-40";

export function FlashCard({
  front,
  back,
  index,
}: {
  front: string;
  back: string;
  index: number;
}) {
  const [flipped, setFlipped] = useState(false);
  const reducedMotion = useReducedMotion();
  const cardId = useId();


  // console.log(back)

  return (
    <div className="space-y-4">
      <div style={{ perspective: 1200 }}>
        <motion.div
          drag={reducedMotion ? false : "x"}
          dragConstraints={{ left: 0, right: 0 }}
          dragElastic={0.15}
          dragMomentum={false}
          dragSnapToOrigin
          style={{ touchAction: "pan-y" }}
        >
          <motion.div
            id={cardId}
            initial={false}
            animate={{ rotateY: reducedMotion ? 0 : flipped ? 180 : 0 }}
            transition={{ duration: reducedMotion ? 0 : 0.45 }}
            className="relative grid"
            style={{ transformStyle: "preserve-3d" }}
          >
            {[
              { label: "Question", content: front, isBack: false },
              { label: "Answer", content: back, isBack: true },
            ].map(({ label, content, isBack }) => {
              const active = flipped === isBack;

              return (
                <div
                  key={label}
                  onClick={() => setFlipped((value) => !value)}
                  aria-hidden={!active}
                  inert={!active}
                  className={`col-start-1 row-start-1 flex min-h-64 min-w-0 flex-col justify-center rounded-xl border p-5 shadow-lg sm:min-h-72 sm:p-6 ${
                    isBack
                      ? "border-accent/30 bg-surface-strong"
                      : "border-border bg-surface-strong"
                  }`}
                  style={{
                    backfaceVisibility: "hidden",
                    transform:
                      isBack && !reducedMotion ? "rotateY(180deg)" : undefined,
                    visibility: reducedMotion && !active ? "hidden" : undefined,
                  }}
                >
                  <p className="mb-4 text-xs font-semibold uppercase tracking-wider text-text-soft">
                    {label} · Card {index + 1}
                  </p>
                  <div className="min-w-0 text-sm text-text sm:text-base">
                    <MathJax dynamic hideUntilTypeset="first">
                      {content}
                    </MathJax>
                  </div>
                </div>
              );
            })}
          </motion.div>
        </motion.div>
      </div>


    </div>
  );
}

export default function Flashcards({ data }: { data: FlashcardSet }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const index = Math.min(currentIndex, Math.max(0, data.cards.length - 1));
  const card = data.cards[index];

  if (!card) {
    return <p className="text-sm text-text-soft">No flashcards available.</p>;
  }

  return (
    <section
      aria-label="Flashcards"
      className="mx-auto w-full max-w-xl space-y-5 p-3 sm:p-5"
    >
      <div className="relative">
        {Array.from({
          length: Math.min(2, data.cards.length - index - 1),
        }).map((_, layer) => (
          <div
            key={layer}
            aria-hidden="true"
            className="pointer-events-none absolute inset-x-0 top-0 min-h-64 rounded-xl border border-border bg-surface-muted sm:min-h-72"
            style={{
              transform: `translateY(${(layer + 1) * 6}px) rotate(${(layer + 1) * 2}deg)`,
            }}
          />
        ))}

        <FlashCard
          key={`${index}:${card.front}:${card.back}`}
          front={card.front}
          back={card.back}
          index={index}
        />
      </div>

      <div className="flex items-center justify-between gap-3">
        <button
          type="button"
          disabled={index === 0}
          onClick={() => setCurrentIndex(index - 1)}
          className={buttonClass}
        >
          Previous
        </button>
        <p role="status" className="text-xs text-text-soft">
          {index + 1} of {data.cards.length}
        </p>
        <button
          type="button"
          disabled={index === data.cards.length - 1}
          onClick={() => setCurrentIndex(index + 1)}
          className={buttonClass}
        >
          Next
        </button>
      </div>
    </section>
  );
}
