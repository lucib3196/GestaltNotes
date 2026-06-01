import type { WorkspaceItem } from "../models/workspace.types";
import { ToolMessage } from "langchain";
export type WorkspaceState = {
  workspaceItems: WorkspaceItem[];
};
export type WorkspaceActions = {
  addWorkspaceItem: (item: WorkspaceItem) => void;
  clearWorkspace: () => void;
  appendToolMessage: (msg: ToolMessage) => void;
};

export type WorkspaceStore = WorkspaceState & WorkspaceActions;
