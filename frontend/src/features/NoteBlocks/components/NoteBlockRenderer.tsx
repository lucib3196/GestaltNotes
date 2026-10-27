import {
  conceptualQuestionSchema,
  derivationSchema,
  extractedQuestionSchema,
  lectureSummarySchema,
  type NoteBlock,
} from "../schemas";
import LectureSummary from "./LectureSummary";
import ExtractedQuestion from "./ExtractedQuestion";
import Derivation from "./Derivation";
import ConceptualQuestion from "./ConceptualQuestion";

export default function NoteBlockRenderer({ block }: { block: NoteBlock }) {
  if (block.schema_version !== 1) {
    return <p>This content version is not supported yet.</p>;
  }

  switch (block.kind) {
    case "lecture_summary": {
      const result = lectureSummarySchema.safeParse(block.content);
      return result.success
        ? <LectureSummary content={result.data} /> : <InvalidBlock />;
    }
    case "extracted_question": {
      const result = extractedQuestionSchema.safeParse(block.content);
      return result.success
        ? <ExtractedQuestion content={result.data} /> : <InvalidBlock />;
    }
    case "derivation": {
      const result = derivationSchema.safeParse(block.content);
      return result.success
        ? <Derivation content={result.data} /> : <InvalidBlock />;
    }
    case "conceptual_question": {
      const result = conceptualQuestionSchema.safeParse(block.content);
      return result.success
        ? <ConceptualQuestion content={result.data} /> : <InvalidBlock />;
    }
    default:
      return <p>This content type is not supported yet.</p>;
  }
}

function InvalidBlock() {
  return <p>This block could not be displayed.</p>;
}
