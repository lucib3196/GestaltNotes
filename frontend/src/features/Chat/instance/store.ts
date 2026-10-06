import { createStore } from "zustand/vanilla";
import { createChatSessionSlice } from "../../../stores/chat/chatSlice";
import { createThreadStore } from "../../../stores/chat/threadSlice";
import type { ChatStore } from "../../../stores/chat/state";

export function createChatStore() {
  return createStore<ChatStore>()((...args) => ({
    ...createChatSessionSlice()(...args),
    ...createThreadStore()(...args),
  }));
}
