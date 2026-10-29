import type { StateCreator } from "zustand";
import type { ChatStore, ChatSlice } from "./state";
import { ConfigSchema } from "./config";

export type ChatSliceCreator = StateCreator<ChatStore, [], [], ChatSlice>;
// course_collection_name:
//         "course_Mechanics 101_76a8ff6248a1487ca75ded3d76dba8fc",
//       embedding_model: "gemini-embedding-001",
//       course_name: "Mechanics 101",
export function createChatSessionSlice<
  Store extends ChatStore = ChatStore,
>(): ChatSliceCreator {
  return (set) => ({
    // Temporary course configuration for testing retrieval in the agent stream.
    config: ConfigSchema.parse({
      course_collection_name: null,
      embedding_model: null,
      course_name: null,
    }),
    assistant: { id: "agent", label: "agent", description: null },
    setModel: (model) =>
      set((state) => ({
        config: ConfigSchema.parse({ ...state.config, model }),
      })),

    draftMessage: null,
    attachments: [],
    pendingPrompt: null,

    setAssistant: (ass) => set({ assistant: ass } as Partial<Store>),

    setDraftMessage: (draftMessage) => set({ draftMessage } as Partial<Store>),

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
        draftMessage: null,
        attachments: [],
      }),

    startNewChat: () =>
      set({
        activeThreadId: null,
        activeThreadStatus: "idle",
        activeThreadError: null,
        draftMessage: null,
        attachments: [],
        pendingPrompt: null,
      }),
    updateConfig: (updates) =>
      set((state) => ({
        config: ConfigSchema.parse({ ...state.config, ...updates }),
      })),
  });
}
