import clsx from "clsx";

export type InputStyleVariant =
    | "default"
    | "outline"
    | "filled"
    | "hidden"
    | "inline"
    | "createQuestion";

type InputStyleConfig = {
    wrapper: string;
    label: string;
    input: string;
};

export const inputStyles: Record<InputStyleVariant, InputStyleConfig> = {
    default: {
        wrapper: "mt-2 w-1/2 min-w-[200px]",
        label: "block text-sm font-medium text-black mb-1",
        input:
            "block w-full rounded-md bg-white/5 px-3 py-1.5 outline outline-1 outline-black placeholder:text-gray-500 focus:outline-indigo-500",
    },

    outline: {
        wrapper: "mt-2 w-1/2 min-w-[200px]",
        label: "block text-sm font-medium text-gray-700 mb-1",
        input:
            "block w-full rounded-md bg-transparent px-3 py-1.5 border border-gray-400 text-black placeholder:text-gray-500 focus:border-indigo-500",
    },

    filled: {
        wrapper: "mt-2 w-1/2 min-w-[200px]",
        label: "block text-sm font-medium text-gray-700 mb-1",
        input:
            "block w-full rounded-md bg-gray-200 px-3 py-1.5 text-black placeholder:text-gray-600 focus:bg-white",
    },

    hidden: {
        wrapper: "mt-0 w-full",
        label: "sr-only",
        input:
            "block w-full bg-transparent px-0 py-0 text-black placeholder:text-gray-600 focus:bg-white",
    },

    inline: {
        wrapper: "w-1/2 min-w-[200px] flex flex-row justify-between",
        label: "block text-sm font-medium text-gray-700 mb-1",
        input:
            "block w-full rounded-md bg-transparent px-3 py-1 border border-gray-400 text-black placeholder:text-gray-500 focus:border-indigo-500",
    },
    createQuestion: {
        wrapper: "w-full flex flex-col gap-1",
        label:
            "text-xs font-semibold uppercase tracking-wide text-slate-600",
        input:
            "block w-full rounded-md bg-white px-3 py-2 text-sm text-slate-900 " +
            "border border-slate-300 shadow-sm " +
            "placeholder:text-slate-400 " +
            "focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20",
    },
};

export type InputComponentProps =
    React.InputHTMLAttributes<HTMLInputElement> & {
        label: string;
        variant?: InputStyleVariant;
        hint?: React.ReactNode;
    };

export function InputTextForm({
    label,
    variant = "default",
    className,
    hint,
    ...props
}: InputComponentProps) {
    const styles = inputStyles[variant];

    return (
        <div className={styles.wrapper}>
            <label htmlFor={props.id} className={styles.label}>
                {label}
            </label>

            <input {...props} className={clsx(styles.input, className)} />

            {hint && <p className="mt-1 text-xs text-gray-500">{hint}</p>}
        </div>
    );
}

export default InputTextForm;
