type ToolActionCardVariant = "sky" | "emerald" | "amber" | "rose" | "slate";

type ToolActionCardProps = {
    title: string;
    label: string;
    value: string;
    variant?: ToolActionCardVariant;
    onClick: (value: string) => void;
};

const variantClasses: Record<
    ToolActionCardVariant,
    { background: string; title: string; label: string; border: string; hoverBorder: string }
> = {
    sky: {
        background: "bg-sky-900/60",
        title: "text-sky-50",
        label: "text-sky-200",
        border: "border-sky-700/70",
        hoverBorder: "hover:border-sky-400",
    },
    emerald: {
        background: "bg-emerald-900/60",
        title: "text-emerald-50",
        label: "text-emerald-200",
        border: "border-emerald-700/70",
        hoverBorder: "hover:border-emerald-400",
    },
    amber: {
        background: "bg-amber-900/60",
        title: "text-amber-50",
        label: "text-amber-200",
        border: "border-amber-700/70",
        hoverBorder: "hover:border-amber-400",
    },
    rose: {
        background: "bg-rose-900/60",
        title: "text-rose-50",
        label: "text-rose-200",
        border: "border-rose-700/70",
        hoverBorder: "hover:border-rose-400",
    },
    slate: {
        background: "bg-slate-800/70",
        title: "text-slate-50",
        label: "text-slate-200",
        border: "border-slate-600/70",
        hoverBorder: "hover:border-slate-400",
    },
};

export function ToolActionCard({
    title,
    label,
    value,
    variant = "sky",
    onClick,
}: ToolActionCardProps) {
    const styles = variantClasses[variant];

    return (
        <button
            type="button"
            title={label}
            aria-label={label}
            onClick={() => onClick(value)}
            className={`group w-full rounded-lg border px-3 py-3 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-accent/40 ${styles.background} ${styles.border} ${styles.hoverBorder}`}
        >
            <p className={`text-sm font-medium ${styles.title}`}>{title}</p>
            <p className={`mt-1 text-xs opacity-0 transition-opacity group-hover:opacity-100 ${styles.label}`}>
                {label}
            </p>
        </button>
    );
}
