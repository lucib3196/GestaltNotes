import Markdown from "../../../../components/Markdown/MarkdownRenderer";
import type { Derivation as DerivationType } from "../../models/lecture.types";
import BaseLectureEntry from "./BaseLectureEntry";

type DerivationProps = {
    derivation: DerivationType;
};

export default function Derivation({ derivation }: DerivationProps) {
    return (
        <BaseLectureEntry
            eyebrow="Derivation"
            title={derivation.derivation_title}
            subtitle={derivation.derivation_stub}
            reference={derivation.reference}
        >
            <ol className="list-decimal space-y-2 pl-5 text-text-muted">
                {derivation.steps.map((step, index) => (
                    <li key={`${derivation.derivation_title}-${index}`}>
                        <Markdown>{step}</Markdown>
                    </li>
                ))}
            </ol>
        </BaseLectureEntry>
    );
}
