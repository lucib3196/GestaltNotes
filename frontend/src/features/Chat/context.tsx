import { createContext, useState, useContext, } from "react";
import type { LectureMetadata } from "../../types/Metadata.types";

export type LectureArtifact = {
    id: string;
    metadata: LectureMetadata;
    page_content: string;
    type: string;
};

type LectureChatContext = {
    sources: LectureArtifact[]
    setSources: (val: LectureArtifact[]) => void
}

const LectureChatContext = createContext<LectureChatContext | undefined>(undefined)


export function LectureChatProvider({ children }: { children: React.ReactNode }) {
    const [sources, setSources] = useState<LectureArtifact[]>([])

    return <LectureChatContext.Provider value={{ sources, setSources }}>
        {children}
    </LectureChatContext.Provider>
}

export function UseLectureChatContext() {
    const context = useContext(LectureChatContext)
    if (context === undefined) {
        throw new Error("LectureChatContext must be used within APP")
    }
    return context;
}