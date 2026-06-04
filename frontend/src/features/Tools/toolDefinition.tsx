import type { ToolName, ToolDefinition } from "./models/tools.types"
import { parseLectureTool } from "../Lectures/utils"
import { HomeworkPreview, LecturePreview } from "../Lectures/tools/LectureTool"
import { parseHomeworkTool } from "../Lectures/utils"
import { parseMultipleChoice, RenderMCQ, saveResponse } from "../MCQ"


export const tools: Partial<Record<ToolName, ToolDefinition<any>>> = {
    retrieve_me116_lecture: {
        parse: parseLectureTool,
        Preview: LecturePreview
    },
    retrieve_me116_homework: {
        parse: parseHomeworkTool,
        Preview: HomeworkPreview
    },
    generate_mcq: {
        parse: parseMultipleChoice,
        Preview: RenderMCQ,
        execute: saveResponse
    }
}
