import type { WorkspaceItem } from "../models/workspace.types";
import { ToolMessage } from "langchain";
import type { SectionTab } from "../../../pages/ChatPage";
export type WorkspaceState = {
  workspaceItems: WorkspaceItem[];
  currentSection: SectionTab;
};
export type WorkspaceActions = {
  addWorkspaceItem: (item: WorkspaceItem) => void;
  clearWorkspace: () => void;
  appendToolMessage: (msg: ToolMessage) => void;

  setCurrentSection: (val: SectionTab) => void;
};

export type WorkspaceStore = WorkspaceState & WorkspaceActions;
