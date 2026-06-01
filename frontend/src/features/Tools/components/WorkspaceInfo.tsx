import { ToolActionCard } from "./ui/ToolActionCard";
import { useChatStore } from "../../Chat/instance/store";
import type { ToolConfig } from "../models/workspaceInfo.types";
import { useState } from "react";

const availableTools: ToolConfig[] = [
    {
        id: "generate_quiz",
        title: "Generate Quiz",
        hoverLabel: "Create a quiz from the current session context",
        prompt: "Generat a medium difficulty quiz of about 3 questions based on the current session ",
    },
];

export default function WorkspaceInfo() {
    const setMessage = useChatStore((s) => s.setExternalMessage);
    const [showHelp, setShowHelp] = useState<boolean>(false);

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
                        variant="rose"
                        onClick={setMessage}
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
                    <span>About Resource & Practice</span>
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
                    </div>
                )}
            </div>
        </div>
    );
}
