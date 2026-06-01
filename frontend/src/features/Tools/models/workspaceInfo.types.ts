import type { SectionTab } from "../../../pages/ChatPage";

export type AvailableTool = "generate_quiz";

export type ToolConfig = {
  id: AvailableTool;
  title: string;
  hoverLabel: string;
  prompt: string;
  section?: SectionTab
};
