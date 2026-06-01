export type AvailableTool = "generate_quiz";

export type ToolConfig = {
  id: AvailableTool;
  title: string;
  hoverLabel: string;
  prompt: string;
};
