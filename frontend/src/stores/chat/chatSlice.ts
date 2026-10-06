import type { StateCreator } from "zustand";
import type { ChatStore, ChatSlice } from "./state";

export type ChatSliceCreator = StateCreator<ChatStore, [], [], ChatSlice>;

export function createChatSessionSlice<
  Store extends ChatStore = ChatStore,
>(): ChatSliceCreator {
  return (set) => ({
    assistant: { id: "agent", label: "agent", description: null },
    draftText: "",
    attachments: [],
    pendingPrompt: null,

    setAssistant: (ass) => set({ assistant: ass } as Partial<Store>),

    setDraftText: (draftText) => set({ draftText } as Partial<Store>),

    addAttachments: (files) =>
      set(
        (state) =>
          ({
            attachments: [
              ...state.attachments,
              ...files.map((file) => ({
                id: crypto.randomUUID(),
                file,
              })),
            ],
          }) as Partial<Store>,
      ),

    removeAttachment: (id) =>
      set(
        (state) =>
          ({
            attachments: state.attachments.filter((item) => item.id !== id),
          }) as Partial<Store>,
      ),

    queuePrompt: (text) =>
      set({
        pendingPrompt: {
          id: crypto.randomUUID(),
          text,
        },
      } as Partial<Store>),

    // Avoid clearing a newer prompt after an older submission finishes.
    clearPendingPrompt: (id) =>
      set((state) =>
        state.pendingPrompt?.id === id ? { pendingPrompt: null } : state,
      ),

    clearDraft: () =>
      set({
        draftText: "",
        attachments: [],
      }),

    startNewChat: () =>
      set({
        activeThreadId: null,
        activeThreadStatus: "idle",
        activeThreadError: null,
        draftText: "",
        attachments: [],
        pendingPrompt: null,
      }),
  });
}
