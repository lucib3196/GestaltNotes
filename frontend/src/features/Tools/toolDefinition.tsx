import type { ToolName, ToolDefinition } from "./models/tools.types"
import { parseLectureTool, LecturePreview } from "./tools/LectureTools"
import { parseMultipleChoice, RenderMCQ, saveResponse } from "../MCQ"


export const tools: Partial<Record<ToolName, ToolDefinition<any>>> = {
    retrieve_me116_lecture: {
        parse: parseLectureTool,
        Preview: LecturePreview
    },
    generate_mcq: {
        parse: parseMultipleChoice,
        Preview: RenderMCQ,
        execute: saveResponse
    }
}
