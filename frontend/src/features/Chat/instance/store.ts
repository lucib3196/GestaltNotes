import { createStore } from "zustand";
import type { ChatState, ChatStore, WorkspaceItem } from "./types";
import { ChatAPI } from "../../../services";
import type { ThreadCreate } from "../../../services";
import { getSupportedToolMessage } from "../tools/utils";
import { TOOL_POLICY } from "../tools/types";

const initialState: ChatState = {
  assistantId: "agent_me116",
  theadId: null,
  thread: null,
  workspaceItems: [],
  sessionKey: 0,
};

export function createChatStore(preloaded?: Partial<ChatState>) {
  return createStore<ChatStore>()((set, get) => ({
    ...preloaded,
    ...initialState,
    setAssistant: (agent) => set({ assistantId: agent }),
    setSessionKey: () => set((state) => ({ sessionKey: state.sessionKey + 1 })),
    setThreadId: (val) =>
      set((state) => ({
        theadId: val,
        thread: val === state.theadId ? state.thread : null,
        workspaceItems: val === state.theadId ? state.workspaceItems : [],
      })),
    setThread: async (id, token) => {
      try {
        const t = await ChatAPI.getThread(id, token);
        set(() => ({ thread: t }));
      } catch (error) {
        throw new Error("Could not fetch thread");
      }
    },
    selectThread: async (id, token) => {
      if (!id) return;
      set({
        theadId: id,
        thread: null,
        workspaceItems: [],
      });
      try {
        const thread = await ChatAPI.getThread(id, token);
        set({ thread });
      } catch (e) {
        set({ thread: null });
        throw e;
      }
    },
    updateThread: async (id, update) => {
      try {
        await ChatAPI.updateThread(id, update);
      } catch (error) {
        throw new Error("Could not generate thread id");
      }
    },
    onThreadId: async (id, token) => {
      const data: ThreadCreate = {
        thread_id: id,
      };
      const created = await get().createdThread(token, data);
      set({
        theadId: created.id,
        thread: created,
        workspaceItems: [],
      });
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
    // Future would be to add more comprehensive logic
    setWorkspaceItems: (item) =>
      set((state) => ({ workspaceItems: [...state.workspaceItems, item] })),
    appendToolMessage: (msg) => {
      // Validate message and ensure that it is what i want to capture
      const parsed = getSupportedToolMessage(msg);
      if (!parsed) return;

      const item: WorkspaceItem = {
        id: crypto.randomUUID(),
        tool: parsed.name,
        rawMsg: msg,
      };
      set((state) => {
        const policy = TOOL_POLICY[parsed.name];

        // basic dedupe by tool-message id if available

        const alreadyExists = state.workspaceItems.some(
          (w) =>
            w.tool === item.tool &&
            w.rawMsg.id &&
            w.rawMsg.id === item.rawMsg.id,
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
}
