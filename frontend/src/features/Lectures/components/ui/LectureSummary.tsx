import Markdown from "../../../../components/Markdown/MarkdownRenderer";
import type { LectureAnalysis } from "../../models/lecture.types";
import BaseLectureEntry from "./BaseLectureEntry";

type LectureSummaryProps = {
    lecture?: LectureAnalysis|null;
};

export default function LectureSummary({ lecture }: LectureSummaryProps) {
    if (!lecture) return;
    return (
        <BaseLectureEntry
            eyebrow="Lecture summary"
            title={lecture.lecture_title}
            subtitle={lecture.lecture_type ?? undefined}
        >
            <div className="leading-relaxed text-text-muted">
                <Markdown>{lecture.lecture_summary}</Markdown>
            </div>

            <SectionList title="Core topics" items={lecture.core_topics} />
            <SectionList
                title="Learning objectives"
                items={lecture.learning_objectives}
            />
            <SectionList
                title="Prerequisites"
                items={lecture.assumed_prerequisites ?? []}
                emptyText="None specified"
            />
        </BaseLectureEntry>
    );
}

function SectionList({
    title,
    items,
    emptyText,
}: {
    title: string;
    items: string[];
    emptyText?: string;
}) {
    return (
        <section>
            <h4 className="mb-2 text-xs font-semibold uppercase text-text-soft">
                {title}
            </h4>

            {items.length > 0 ? (
                <ul className="list-disc space-y-1 pl-5 text-text-muted">
                    {items.map((item) => (
                        <li key={item}><Markdown>{item}</Markdown></li>
                    ))}
                </ul>
            ) : (
                <p className="text-text-soft">{emptyText ?? "No items found."}</p>
            )}
        </section>
    );
}
