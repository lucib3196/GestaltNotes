import type { TopicStarter } from "../models/starters.types";

export type StarterState = {
  selectedState: TopicStarter | null;
  validStates: TopicStarter[];
};

export type StarterActions = {
  setSelectedState: (t: TopicStarter) => void;
};

export type StarterStore = StarterState & StarterActions;
