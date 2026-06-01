import clsx from "clsx";

export type NavStepButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
    children: React.ReactNode;
};

export function NavStepButton({
    children,
    className,
    type = "button",
    ...rest
}: NavStepButtonProps) {
    return (
        <button
            type={type}
            className={clsx(
                "rounded-md border border-border bg-surface px-2.5 py-1 text-xs text-text-muted transition-colors hover:border-border-strong hover:text-text disabled:cursor-not-allowed disabled:opacity-40",
                className,
            )}
            {...rest}
        >
            {children}
        </button>
    );
}
