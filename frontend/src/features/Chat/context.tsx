import { createContext, useState, useContext, } from "react";
import type { LectureMetadata } from "../../types/Metadata.types";


export type ValidAgent = "agent_me135" | "agent_me118";

export type LectureArtifact = {
    id: string;
    metadata: LectureMetadata;
    page_content: string;
    type: string;
};

type LectureChatContext = {
    agent: ValidAgent
    setAgent: (val: ValidAgent) => void
    threadId: string | null;
    setThreadId: (val: string | null) => void;
    sources: LectureArtifact[]
    setSources: (val: LectureArtifact[]) => void
}

const LectureChatContext = createContext<LectureChatContext | undefined>(undefined)


export function LectureChatProvider({ children }: { children: React.ReactNode }) {
    const [sources, setSources] = useState<LectureArtifact[]>([])
    const [threadId, setThreadId] = useState<string | null>(null);
    const [agent, setAgent] = useState<ValidAgent>("agent_me135")

    return <LectureChatContext.Provider value={{ sources, setSources, agent, setAgent, threadId, setThreadId }}>
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