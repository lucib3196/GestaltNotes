import { useEffect, useMemo, useState } from "react";
import clsx from "clsx";
import type { WorkspaceItem } from "../../Chat/instance/types";
import { RenderToolCalls } from "./RenderToolCalls";
import { NavStepButton } from "../../../components/Button";

type WorkspaceItemsCarouselVariant = "default" | "accent" | "subtle";

const containerVariantClasses: Record<WorkspaceItemsCarouselVariant, string> = {
    default: "rounded-lg border border-border bg-surface/40 p-3",
    accent:
        "rounded-lg border border-accent/35 bg-gradient-to-br from-surface/70 via-surface to-surface-muted/60 p-3 shadow-soft",
    subtle: "rounded-lg border border-border/70 bg-surface-muted/50 p-3",
};

type WorkspaceItemsCarouselProps = {
    items: WorkspaceItem[] | WorkspaceItem | null | undefined;
    sectionLabel?: string;
    itemLabel?: string;
    emptyLabel?: string;
    heightClassName?: string;
    variant?: WorkspaceItemsCarouselVariant;
    className?: string;
};

export function WorkspaceItemsCarousel({
    items,
    sectionLabel = "Items",
    itemLabel = "Item",
    emptyLabel = "No items available yet.",
    heightClassName = "h-[72vh]",
    variant = "default",
    className,
}: WorkspaceItemsCarouselProps) {
    const normalizedItems = useMemo(() => {
        if (!items) return [];
        return Array.isArray(items) ? items : [items];
    }, [items]);

    const [index, setIndex] = useState(0);

    const total = normalizedItems.length;
    const hasItem = total > 0;
    const clampedIndex = hasItem ? Math.min(index, total - 1) : 0;
    const currentItem = hasItem ? normalizedItems[clampedIndex] : null;

    useEffect(() => {
        if (!hasItem) {
            setIndex(0);
            return;
        }
        if (index > total - 1) {
            setIndex(total - 1);
        }
    }, [hasItem, index, total]);

    const goPrev = () => setIndex((prev) => Math.max(0, prev - 1));
    const goNext = () => setIndex((prev) => Math.min(total - 1, prev + 1));

    return (
        <div className={clsx("flex min-h-0 flex-col", heightClassName, className)}>
            <div
                className={clsx(
                    "mb-3 flex items-center justify-between border-b border-border pb-2",
                    containerVariantClasses[variant],
                )}
            >
                <p className="text-xs uppercase tracking-[0.16em] text-text-soft">
                    {hasItem
                        ? `${itemLabel} ${clampedIndex + 1} of ${total}`
                        : sectionLabel}
                </p>

                <div className="flex items-center gap-2">
                    <NavStepButton
                        onClick={goPrev}
                        disabled={!hasItem || clampedIndex === 0}
                        aria-label={`Previous ${itemLabel.toLowerCase()}`}
                    >
                        Prev
                    </NavStepButton>
                    <NavStepButton
                        onClick={goNext}
                        disabled={!hasItem || clampedIndex === total - 1}
                        aria-label={`Next ${itemLabel.toLowerCase()}`}
                    >
                        Next
                    </NavStepButton>
                </div>
            </div>

            <div className="min-h-0 flex-1 overflow-y-auto pr-1">
                {!currentItem ? (
                    <p className="rounded-md border border-border/60 bg-surface-muted/40 px-3 py-2 text-text-soft">
                        {emptyLabel}
                    </p>
                ) : (
                    <RenderToolCalls key={currentItem.id} msg={currentItem.rawMsg} />
                )}
            </div>
        </div>
    );
}
