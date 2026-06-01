import { create } from "zustand";
import { HEAT_TRANSFER_CONVERSATION_STARTERS } from "../constants/heatTransferStarter";
import type { StarterStore, StarterState } from "./types";

const initialState: StarterState = {
  selectedState: HEAT_TRANSFER_CONVERSATION_STARTERS.at(-1) ?? null,
  validStates: HEAT_TRANSFER_CONVERSATION_STARTERS,
};

export const useStarterStore = create<StarterStore>()((set) => ({
  ...initialState,
  setSelectedState: (t) => set({ selectedState: t }),
}));
