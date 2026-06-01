import { useStarterStore } from "../instance/store";
import { IoIosArrowDropdownCircle, IoIosArrowDroprightCircle } from "react-icons/io";
import { useState } from "react";
import { useChatStore } from "../../Chat/instance/store";
export default function StarterView() {
    const validStarter = useStarterStore((s) => s.validStates);
    const setSelectedStarter = useStarterStore((s) => s.setSelectedState);
    const currentStarter = useStarterStore((s) => s.selectedState);
    const [openStarterId, setOpenStarterId] = useState<string | null>(currentStarter?.id ?? null);
    const sendMessage = useChatStore((s) => s.setExternalMessage)

    const handleStarterClick = (starter: { id: string }) => {
        const isOpen = openStarterId === starter.id;
        setOpenStarterId(isOpen ? null : starter.id);
        setSelectedStarter(starter as any);
    };

    return (
        <section className="rounded-lg border border-border bg-surface p-4 shadow-soft">
            <h2 className="mb-3 text-sm font-semibold uppercase tracking-[0.12em] text-text-soft">
                Review Concepts
            </h2>
            <p className="mb-3 text-xs text-text-soft">
                Choose a starter to prefill chat ideas, or click any option below to send it instantly.
            </p>

            <div className="space-y-2">
                {validStarter.map((starter) => {
                    const isSelected = currentStarter?.id === starter.id;
                    const isOpen = openStarterId === starter.id;

                    return (
                        <div key={starter.id} className="rounded-md border border-border bg-surface-muted">
                            <button
                                type="button"
                                onClick={() => handleStarterClick(starter)}
                                className={`flex w-full items-center justify-between rounded-md px-3 py-2 text-left text-sm transition-colors duration-base ease-base ${isSelected
                                    ? "border-accent bg-accent/10 text-accent"
                                    : "text-text hover:text-accent"
                                    }`}
                            >
                                <span>{starter.title}</span>
                                {isOpen ? (
                                    <IoIosArrowDropdownCircle className="h-5 w-5 shrink-0" />
                                ) : (
                                    <IoIosArrowDroprightCircle className="h-5 w-5 shrink-0" />
                                )}
                            </button>

                            {isOpen && (

                                <div className="space-y-1 border-t border-border px-3 py-2 text-sm text-text-soft">
                                    {starter.starters.map((value, idx) => (
                                        <div key={`${starter.id}-${idx}`} role="button" onClick={() => sendMessage(value)} className="rounded-sm bg-surface px-2 py-1 transition-colors duration-base ease-base hover:bg-accent/10 hover:text-accent">
                                            {value}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </section>
    );
}
