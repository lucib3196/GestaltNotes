
import { createLectureStore } from "./store";
import { type StoreApi } from "zustand";
import type { LectureState, LectureStore, } from "./types";
import React, { createContext, useRef, useContext } from "react";
import { useStore } from "zustand";

const LectureContext = createContext<StoreApi<LectureStore> | null>(null)


export function LectureProvider({
    children, initialState
}: { children: React.ReactNode, initialState?: Partial<LectureState> }) {
    const storeRef = useRef<StoreApi<LectureStore> | null>(null)

    if (!storeRef.current) {
        storeRef.current = createLectureStore(initialState);
    }
    return (
        <LectureContext.Provider value={storeRef.current}>
            {children}
        </LectureContext.Provider>
    );
}

export function useLectureStore<T>(
    selector: (state: LectureStore) => T
): T {
    const store = useContext(LectureContext);
    if (!store) throw new Error("useQuestionCreate must be used within QuestionCreateProvider");
    return useStore(store, selector);
}