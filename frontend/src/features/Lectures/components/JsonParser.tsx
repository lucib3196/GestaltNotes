import LectureSummary from "./ui/LectureSummary";
import Derivation from "./ui/Derivation";
import ConceptualQuestion from "./ui/ConceptualQuestion";
import ExtractedQuestions from "./ui/ExtractedQuestions";
import { useParsedLecture } from "../hooks/hooks";
import type { FileEntry } from "../models/lecture.types";
import { useState, useMemo, useEffect } from "react";
import { NavStepButton } from "../../../components/Button";
import type { ParsedLecture } from "../models/lecture.types";

type NormalizedLectureItem =
  | {
    type: "analysis";
    item: ParsedLecture["lecture_analysis"];
  }
  | {
    type: "derivation";
    item: ParsedLecture["derivations"][number];
  }
  | {
    type: "conceptualQuestion";
    item: ParsedLecture["conceptual_questions"][number];
  }
  | {
    type: "extractedQuestion";
    item: ParsedLecture["extracted_questions"][number];
  };

const renderItem = (entry: NormalizedLectureItem | null, index: number) => {
  if (!entry) return;
  switch (entry.type) {
    case "analysis":
      return <LectureSummary key={index} lecture={entry.item ?? null} />;

    case "derivation":
      return <Derivation key={index} derivation={entry.item} />;

    case "conceptualQuestion":
      return <ConceptualQuestion key={index} question={entry.item} />;

    case "extractedQuestion":
      return <ExtractedQuestions key={index} question={entry.item} />;

    default:
      return null;
  }
};
export default function LectureJson({ file }: { file?: FileEntry | null }) {
  const { lecture, loading, error } = useParsedLecture(file);
  const [index, setIndex] = useState(0);
  const normalizedItems = useMemo<NormalizedLectureItem[]>(() => {
    if (!lecture) return [];

    return [
      {
        type: "analysis",
        item: lecture.lecture_summary,
      },
      ...lecture.derivations.map((item) => ({
        type: "derivation" as const,
        item,
      })),
      ...lecture.conceptual_questions.map((item) => ({
        type: "conceptualQuestion" as const,
        item,
      })),
      ...lecture.extracted_questions.map((item) => ({
        type: "extractedQuestion" as const,
        item,
      })),
      ...lecture.questions.map((item) => ({
        type: "extractedQuestion" as const,
        item,
      })),
    ].filter((v) => v.item);
  }, [lecture]);
  const totalItems = normalizedItems.length;

  const hasItem = totalItems > 0;
  const clampedIndex = hasItem ? Math.min(index, totalItems - 1) : 0;
  const currentItem = hasItem ? normalizedItems[clampedIndex] : null;


  useEffect(() => {
    if (!hasItem) {
      setIndex(0);
      return;
    }
    if (index > totalItems - 1) {
      setIndex(totalItems - 1);
    }
  }, [hasItem, index, totalItems]);

  const goPrev = () => setIndex((prev) => Math.max(0, prev - 1));
  const goNext = () => setIndex((prev) => Math.min(totalItems - 1, prev + 1));

  if (!file) {
    return (
      <div className="rounded-lg border border-border bg-surface p-4 text-text-muted">
        No lecture JSON found.
      </div>
    );
  }
  if (loading || !lecture) {
    return (
      <div className="rounded-lg border border-border bg-surface p-4 text-text-muted">
        Loading lecture JSON...{error}
      </div>
    );
  }

  return (
    <section className="rounded-lg border border-border bg-surface-muted/60 p-3 shadow-sm">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase text-text-soft">
            Lecture cards
          </p>
          <p className="text-sm text-text-muted">
            {hasItem
              ? `${clampedIndex + 1} of ${totalItems}`
              : "No cards available"}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <NavStepButton
            onClick={goPrev}
            disabled={!hasItem || clampedIndex === 0}
            aria-label="Previous lecture card"
          >
            Prev
          </NavStepButton>
          <NavStepButton
            onClick={goNext}
            disabled={!hasItem || clampedIndex === totalItems - 1}
            aria-label="Next lecture card"
          >
            Next
          </NavStepButton>
        </div>
      </div>

      <div className="overflow-hidden rounded-lg">
        {renderItem(currentItem, index)}
      </div>
    </section>
  );
}
