import type { ToolName } from "./tools.types";
import { ToolMessage } from "langchain";

export type WorkspaceItem = {
  id: string;
  tool: ToolName;
  rawMsg: ToolMessage;
};
