import { useStarterStore } from "../instance/store";
export default function StarterView() {
    const validStarter = useStarterStore((s) => s.validStates);
    const setSelectedStarter = useStarterStore((s) => s.setSelectedState)
    const currentStarter = useStarterStore((s) => s.selectedState)


    return (
        <section className="rounded-lg border border-border bg-surface p-4 shadow-soft">
            <h2 className="mb-3 text-sm font-semibold uppercase tracking-[0.12em] text-text-soft">
                Review Concepts
            </h2>
            <div className="space-y-2">
                {validStarter.map((starter) => {
                    const isSelected = currentStarter?.id === starter.id;

                    return (
                        <div
                            role="button"
                            onClick={() => setSelectedStarter(starter)}
                            key={starter.id}
                            className={`rounded-md border px-3 py-2 text-sm transition-colors duration-base ease-base ${isSelected
                                ? "border-accent bg-accent/10 text-accent"
                                : "border-border bg-surface-muted text-text hover:border-border-strong hover:text-accent"
                                }`}
                        >
                            {starter.title}
                        </div>
                    );
                })}
            </div>
           
        </section>
    );
}
