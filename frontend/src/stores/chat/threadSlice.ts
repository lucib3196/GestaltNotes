import type { StateCreator } from "zustand";
import type { ChatStore, ThreadSlice } from "./state";
import { threadsById } from "./utils";

export type ThreadSliceCreator<
  Store extends ChatStore = ChatStore,
  Slice = ThreadSlice,
> = StateCreator<Store, [], [], Slice>;

export function createThreadStore<
  Store extends ChatStore = ChatStore,
>(): ThreadSliceCreator<Store, ThreadSlice> {
  return (set) => ({
    threadsById: {},
    threadIds: [],
    activeThreadId: null,
    listStatus: "idle",
    listError: null,
    activeThreadStatus: "idle",
    activeThreadError: null,

    selectThread: (id) =>
      set((state) => {
        if (state.activeThreadId === id) return state;

        return {
          activeThreadId: id,
          activeThreadStatus: "idle",
          activeThreadError: null,
        } as Partial<Store>;
      }),
    setThreads: (threads) =>
      set(
        (state) =>
          ({
            threadsById: {
              ...state.threadsById,
              ...threadsById(threads),
            },
            threadIds: [...new Set(threads.map((thread) => thread.id))],
          }) as Partial<Store>,
      ),
    upsertThread: (thread) =>
      set(
        (state) =>
          ({
            threadsById: {
              ...state.threadsById,
              [thread.id]: thread,
            },
            threadIds: state.threadIds.includes(thread.id)
              ? state.threadIds
              : [thread.id, ...state.threadIds],
          }) as Partial<Store>,
      ),
    removeThread: (id) =>
      set((state) => {
        const threadsById = { ...state.threadsById };
        delete threadsById[id];

        return {
          threadsById,
          threadIds: state.threadIds.filter((threadId) => threadId !== id),
          ...(state.activeThreadId === id
            ? {
                activeThreadId: null,
                activeThreadStatus: "idle" as const,
                activeThreadError: null,
                draftText: "",
                attachments: [],
                pendingPrompt: null,
              }
            : {}),
        } as Partial<Store>;
      }),
    setListStatus: (status, error) =>
      set({
        listStatus: status,
        listError:
          status === "error" ? (error ?? "Could not load chats") : null,
      } as Partial<Store>),

    setActiveThreadStatus: (status, error) =>
      set({
        activeThreadStatus: status,
        activeThreadError:
          status === "error" ? (error ?? "Could not load chat") : null,
      } as Partial<Store>),
  });
}
