import type { ToolMessage } from "langchain";
import type { RenderPreviewProps, ToolExecute } from "../../Chat/tools";

import { extractToolPayload } from "../../Chat/utils";
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
    console.log("Parsing multiple choice",)
    const raw = extractToolPayload(msg) as MultipleChoiceQuestionToolResponse;
    console.log("Parsed", raw)
    return raw;
}

export const saveResponse: ToolExecute<
    MultipleChoiceQuestionToolResponse
> = async (args) => {
    try {
        const payload: GeneratedContentSaveRequest = {
            qpayload: args.payload,
            thread_id: args.ctx?.threadId,
        };
        await MCQClient.saveQuestions(payload, args.ctx?.token);
        toast.success("Saving Response");
    } catch (error) {
        const message =
            error instanceof Error ? error.message : "Failed to save questions";
        toast.error(message);
        throw error;
    }
};

export function RenderMCQ({
    payload,
    onApprove,
}: RenderPreviewProps<MultipleChoiceQuestionToolResponse>) {
    const Qpayload = payload?.payload ?? [];

    if (!Qpayload.length) {
        return "Loading";
    }

    const onSubmit = (submission: MultipleChoiceQuestionSubmitted[]) => {
        try {
            const data = {
                payload: submission
            };
            onApprove?.(data);
        } catch (error) {
            const message =
                error instanceof Error ? error.message : "Failed to submit MCQ responses";
            toast.error(message);
        }
    };


    return (
        <div className="w-full space-y-5 rounded-xl border border-border bg-surface p-3">
            <h4 className="text-sm font-semibold text-text">
                Practice Your Understanding
            </h4>
            <RenderMCQList questions={Qpayload} onSubmitBatch={onSubmit} />
        </div>
    );
}
