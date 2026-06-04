import type { SectionTab } from "../../../pages/ChatPage";

export type AvailableTool = "generate_quiz" | "explain_previous_homework"|"retrieve_lecture";

export type ToolConfig = {
  id: AvailableTool;
  title: string;
  hoverLabel: string;
  prompt: string;
  section?: SectionTab;
  color?: string;
};
