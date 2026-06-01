import { create } from "zustand";
import type { WorkspaceItem } from "../models/workspace.types";
import type { WorkspaceState, WorkspaceStore } from "./types";
import { getSupportedToolMessage } from "../utils";
import { TOOL_POLICY } from "../models/tools.types";

const initialState: WorkspaceState = {
  workspaceItems: [],
  currentSection: "info",
};

export const useWorkspaceStore = create<WorkspaceStore>()((set) => ({
  ...initialState,
  setCurrentSection: (val) => set({ currentSection: val }),
  clearWorkspace: () => set(() => ({ workspaceItems: [] })),
  addWorkspaceItem: (item) =>
    set((state) => ({ workspaceItems: [...state.workspaceItems, item] })),
  appendToolMessage: (msg) => {
    const parsed = getSupportedToolMessage(msg);
    if (!parsed) return;

    const item: WorkspaceItem = {
      id: crypto.randomUUID(),
      tool: parsed.name,
      rawMsg: msg,
    };

    set((state) => {
      const policy = TOOL_POLICY[parsed.name];

      const alreadyExists = state.workspaceItems.some(
        (w) =>
          w.tool === item.tool && w.rawMsg.id && w.rawMsg.id === item.rawMsg.id,
      );
      if (alreadyExists) return state;

      if (policy === "replace") {
        return {
          workspaceItems: [
            ...state.workspaceItems.filter((w) => w.tool !== item.tool),
            item,
          ],
        };
      }

      if (policy === "replace_and_push") {
        return {
          workspaceItems: [
            item,
            ...state.workspaceItems.filter((w) => w.tool !== item.tool),
          ],
        };
      }

      return {
        workspaceItems: [...state.workspaceItems, item],
      };
    });
  },
}));
