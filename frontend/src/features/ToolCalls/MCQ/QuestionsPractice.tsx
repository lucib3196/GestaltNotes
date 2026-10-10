import { useChatStore } from "../../Chat/instance";
import MultipleChoiceQuiz from "./MultipleChoiceQuiz";
import type {
  MultipleChoiceSet,
  QuizSaveHandler,
  QuizSubmission,
} from "./types";
import { buildReviewPrompt } from "./utils";

export type QuestionsPracticeProps = {
  data: MultipleChoiceSet;
  onSave?: QuizSaveHandler;
  saveEnabled?: boolean;
};

export default function QuestionsPractice({
  data,
  onSave,
  saveEnabled = false,
}: QuestionsPracticeProps) {
  const setDraftText = useChatStore((state) => state.setDraftText);
  const draftText = useChatStore((state) => state.draftText);
  function requestReview(submission: QuizSubmission) {
    if (draftText)
      throw new Error("Another review is waiting to be submitted.");
    setDraftText(buildReviewPrompt(data, submission));
  }
  return (
    <MultipleChoiceQuiz
      data={data}
      onReview={requestReview}
      onSave={onSave}
      saveEnabled={saveEnabled}
    />
  );
}
