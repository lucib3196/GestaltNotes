
import { createChatStore } from "./store";
import { type StoreApi } from "zustand";
import { type ChatStore, type ChatState } from "./types";
import React, { createContext, useRef, useContext } from "react";
import { useStore } from "zustand";

const ChatContext = createContext<StoreApi<ChatStore> | null>(null)


export function ChatProvider({
    children, initialState
}: { children: React.ReactNode, initialState?: Partial<ChatState> }) {
    const storeRef = useRef<StoreApi<ChatStore> | null>(null)

    if (!storeRef.current) {
        storeRef.current = createChatStore(initialState);
    }
    return (
        <ChatContext.Provider value={storeRef.current}>
            {children}
        </ChatContext.Provider>
    );
}

export function useChatContext<T>(
    selector: (state: ChatStore) => T
): T {
    const store = useContext(ChatContext);
    if (!store) throw new Error("useQuestionCreate must be used within QuestionCreateProvider");
    return useStore(store, selector);
}