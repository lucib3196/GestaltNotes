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
  const setDraftMessage = useChatStore((state) => state.setDraftMessage);
  const draftMessage = useChatStore((state) => state.draftMessage);
  function requestReview(submission: QuizSubmission) {
    if (draftMessage)
      throw new Error("Another review is waiting to be submitted.");
    setDraftMessage({
      text: buildReviewPrompt(data, submission),
      internal: true,
    });
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
