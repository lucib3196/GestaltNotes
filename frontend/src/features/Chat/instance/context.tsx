import { createContext, useContext, useRef } from "react";
import type { ReactNode } from "react";
import { useStore } from "zustand";
import type { ChatStore } from "../../../stores/chat/state";
import { createChatStore } from "./store";

const ChatContext = createContext<ReturnType<typeof createChatStore> | null>(
  null,
);

export function ChatProvider({ children }: { children: ReactNode }) {
  const storeRef = useRef<ReturnType<typeof createChatStore> | null>(null);

  if (storeRef.current === null) {
    storeRef.current = createChatStore();
  }

  return (
    <ChatContext.Provider value={storeRef.current}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChatStore<T>(selector: (state: ChatStore) => T): T {
  const store = useContext(ChatContext);

  if (!store) {
    throw new Error("useChatStore must be used within ChatProvider");
  }

  return useStore(store, selector);
}
