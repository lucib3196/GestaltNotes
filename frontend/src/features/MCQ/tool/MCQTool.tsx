import type { ToolMessage } from "langchain";
import type { RenderPreviewProps, ToolExecute } from "../../Chat/tools";

import { extractToolPayload } from "../../Chat/utils";
import { RenderMCQSingle } from "../index";
import { Button } from "../../../components/Button";
import { RenderMCQList } from "../components/MCQ";

import { toast } from "react-toastify";
import type {
    MultipleChoiceQuestionToolResponse,
    GeneratedContentSaveRequest,

} from "../index";
import type { MultipleChoiceQuestionSubmitted } from "../../MCQ/api/mcq.types";
import { MCQClient } from "../index";



export function parseMultipleChoice(
    msg: ToolMessage,
): MultipleChoiceQuestionToolResponse {
    // Eventually add tigher guard railes for this
    const raw = extractToolPayload(msg) as MultipleChoiceQuestionToolResponse;
    return raw;
}



export const saveResponse: ToolExecute<
    MultipleChoiceQuestionToolResponse
> = async (args) => {

    const payload: GeneratedContentSaveRequest
        = {
        qpayload: args.payload,
        thread_id: args.ctx?.threadId
    }
    await MCQClient.saveQuestions(payload, args.ctx?.token)
    toast.success(`Saving to backend`);
};

export function RenderMCQ({
    payload,
    onApprove,
}: RenderPreviewProps<MultipleChoiceQuestionToolResponse>) {
    const Qpayload = payload.payload;

    if (!Qpayload) {
        return "Loading";
    }
    const saveQuestions = () => {
        console.log("Saving Questions")
    }

    const onSubmit = (submission: MultipleChoiceQuestionSubmitted[]) => {
        // Prepare final payload for submission
        console.log("Submitted in tool")
        console.log(submission, "Final payload")
    }


    return (
        <div className="w-full space-y-3 rounded-xl border border-border bg-surface p-3">
            <h4 className="text-sm font-semibold text-text">
                Practice Your Understanding
            </h4>
            <RenderMCQList questions={Qpayload} onSubmitBatch={onSubmit} />
        </div>
    );
}
