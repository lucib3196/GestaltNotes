import type { ChatState, ChatStore } from "./types";

import type { ThreadStore, ThreadState } from "./types";
import { create } from "zustand";

const initialThreadState: ThreadState = {
  threadId: null,
  thread: null,
  threads: [],
};
export const useThreadStore = create<ThreadStore>()((set) => ({
  ...initialThreadState,

  setThreadId: (threadId) =>
    set({
      threadId,
    }),

  setThread: (thread) => {
    set({
      thread,
      threadId: thread?.id ?? null,
    });
  },

  setThreads: (threads) =>
    set({
      threads,
    }),

  clearThread: () =>
    set({
      threadId: null,
      thread: null,
    }),

  updateThread: (update) =>
    set((state) => ({
      thread: state.thread?.id === update.id ? update : state.thread,

      threads: state.threads.map((thread) =>
        thread.id === update.id ? update : thread,
      ),
    })),
}));

const initialChatState: ChatState = {
  assistantId: "agent_me116",
};

export const useChatStore = create<ChatStore>()((set) => ({
  ...initialChatState,

  setAssistant: (assistant) =>
    set({
      assistantId: assistant,
    }),
  setExternalMessage: (val) => set({ externalMessage: val }),
}));
