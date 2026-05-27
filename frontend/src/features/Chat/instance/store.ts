import { createStore } from "zustand";
import type { ChatState, ChatStore } from "./types";
import { ChatAPI } from "../../../services";
import type { ThreadCreate } from "../../../services";

const initialState: ChatState = {
  theadId: null,
};

export function createChatStore(preloaded?: Partial<ChatState>) {
  return createStore<ChatStore>()((set) => ({
    ...preloaded,
    ...initialState,
    setThreadId: (val) => set({ theadId: val }),
    onThreadId: (val) => {
      console.log(val);
    },
    createdThread: async (token: string, data: ThreadCreate) => {
      try {
        const res = await ChatAPI.createThread(data, token);
        return res;
      } catch (error) {
        throw new Error("Could not generate thread id");
      }
    },
    getUserThreads: async (token: string) => {
      try {
        return await ChatAPI.listMyThreads(token);
      } catch (error) {
        throw new Error("Could not load user threads");
      }
    },
    getUserThreadMessages: async (token: string, threadId: string) => {
      try {
        return await ChatAPI.getMessages(token, threadId);
      } catch (error) {
        throw new Error("Could not load thread messages");
      }
    },
  }));
}
