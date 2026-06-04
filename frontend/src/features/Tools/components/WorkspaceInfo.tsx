import { ToolActionCard } from "./ui/ToolActionCard";
import { useChatStore } from "../../Chat/instance/store";
import type { ToolConfig } from "../models/workspaceInfo.types";
import { useState } from "react";
import { useWorkspaceStore } from "../instance/store";
import type { SectionTab } from "../../../pages/ChatPage";
import type { ToolActionCardVariant } from "./ui/ToolActionCard";
const availableTools: ToolConfig[] = [
    {
        id: "generate_quiz",
        title: "Build a Practice Quiz",
        hoverLabel: "Generate focused quiz questions from the current chat and study context",
        prompt: "Create a medium-difficulty practice quiz with about 3 questions based on the current session. Include answers and brief explanations for each question.",
        section: "practice",
        color: "emerald"
    },
    {
        id: "explain_previous_homework",
        title: "Explain Homework Concepts",
        hoverLabel: "Use AI to break down previous homework topics and connect them to core concepts",
        prompt: "Explain Homework 1 and the core concepts it covers. Highlight the key ideas, common mistakes, and how the problems connect to the current topic.",
        section: "resource",
        color: "amber"
    },
    {
        id: "explain_previous_homework",
        title: "Find Related Practice",
        hoverLabel: "Ask AI to locate homework-style questions for a specific concept",
        prompt: "Find homework-style questions that cover conduction. Include the relevant source or context when available, then summarize what each question is testing.",
        section: "resource",
        color: "rose"
    },
    {
        id: "retrieve_lecture",
        title: "Retrieve Relevant Lectures",
        hoverLabel: "Search lecture notes and explain the most relevant material with AI",
        prompt: "Retrieve the most relevant lecture material about the main modes of heat transfer, then explain the key ideas and how they relate to each other.",
        section: "resource"
    },
];

export default function WorkspaceInfo() {
    const setMessage = useChatStore((s) => s.setExternalMessage);
    const setCurrentSection = useWorkspaceStore((s) => s.setCurrentSection)
    const [showHelp, setShowHelp] = useState<boolean>(false);


    const handleClick = (val: string, section?: SectionTab) => {
        setMessage(val)
        if (section) {
            setCurrentSection(section)
        }


    }

    return (
        <div className="flex h-full min-h-0 flex-col gap-4 overflow-y-auto pr-1">
            <h3 className="text-sm font-semibold text-text">Available Actions</h3>
            <div className="mt-3 grid grid-cols-1 gap-3">
                {availableTools.map((tool) => (
                    <ToolActionCard
                        key={tool.id}
                        title={tool.title}
                        label={tool.hoverLabel}
                        value={tool.prompt}
                        variant={tool.color as ToolActionCardVariant}
                        onClick={() => handleClick(tool.prompt, tool.section)}
                    />
                ))}
            </div>

            <div className="mt-auto rounded-lg border border-border bg-surface/30 p-3">
                <button
                    type="button"
                    onClick={() => setShowHelp((prev) => !prev)}
                    className="flex w-full items-center justify-between rounded-md border border-border bg-surface px-3 py-2 text-sm font-medium text-text transition-colors hover:bg-surface/80 active:scale-[0.99]"
                    aria-expanded={showHelp}
                    aria-controls="workspace-info-help"
                >
                    <span>About Resource, Practice & Final Review</span>
                    <span className="text-xs text-text-soft">{showHelp ? "Hide" : "Show"}</span>
                </button>

                {showHelp && (
                    <div id="workspace-info-help" className="mt-3 space-y-3">
                        <section className="rounded-md border border-border bg-surface/40 p-3">
                            <h3 className="text-sm font-semibold text-text">Resource</h3>
                            <p className="mt-1 text-sm text-text-soft">
                                The Resource section is a live preview of retrieved lecture notes,
                                homework, and other supplemental resources based on the current
                                chat session.
                            </p>
                        </section>

                        <section className="rounded-md border border-border bg-surface/40 p-3">
                            <h3 className="text-sm font-semibold text-text">Practice</h3>
                            <p className="mt-1 text-sm text-text-soft">
                                The Practice section shows generated content from available actions.
                                Right now, only Generate Quiz is available, with more tools coming soon.
                            </p>
                        </section>

                        <section className="rounded-md border border-border bg-surface/40 p-3">
                            <h3 className="text-sm font-semibold text-text">Final Review</h3>
                            <p className="mt-1 text-sm text-text-soft">
                                The Final Review section provides guided wrap-up prompts to help you
                                summarize key ideas, identify weak spots, and prepare for exams or
                                assignments based on the current session context.
                            </p>
                        </section>
                    </div>
                )}
            </div>
        </div>
    );
}
