
import { createGenContentStore } from "./store";
import { type StoreApi } from "zustand";
import type { GeneratedContentState, GeneratedContentStore } from "./types";
import React, { createContext, useRef, useContext } from "react";
import { useStore } from "zustand";

const ChatContext = createContext<StoreApi<GeneratedContentStore> | null>(null)


export function GenContentProvider({
    children, initialState
}: { children: React.ReactNode, initialState?: Partial<GeneratedContentState> }) {
    const storeRef = useRef<StoreApi<GeneratedContentStore> | null>(null)

    if (!storeRef.current) {
        storeRef.current = createGenContentStore(initialState);
    }
    return (
        <ChatContext.Provider value={storeRef.current}>
            {children}
        </ChatContext.Provider>
    );
}

export function useGenContentProvider<T>(
    selector: (state: GeneratedContentStore) => T
): T {
    const store = useContext(ChatContext);
    if (!store) throw new Error("useGenContentProvider must be used within QuestionCreateProvider");
    return useStore(store, selector);
}