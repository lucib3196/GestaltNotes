import type { ToolName, ToolDefinition } from "./types"
import { parseLectureTool, LecturePreview } from "./LectureTool"
import { parseMultipleChoice, RenderMCQ, } from "./MCQTool"

export const tools: Partial<Record<ToolName, ToolDefinition<any>>> = {
    retrieve_me116_lecture: {
        parse: parseLectureTool,
        Preview: LecturePreview
    },
    generate_mcq: {
        parse: parseMultipleChoice,
        Preview: RenderMCQ
    }

}
