import {
    type ButtonColor,
    type ButtonSize,
    colorClasses,
    sizeClasses,
    tabToggleBaseClasses,
    tabToggleStateClasses
} from "./config";
import clsx from "clsx";

export type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
    children: React.ReactNode;
    color?: ButtonColor;
    size?: ButtonSize;
};

export default function Button({
    children,
    color = "primary",
    size = "md",
    ...rest
}: ButtonProps) {
    return (
        <button
            className={clsx(
                "rounded font-semibold transition-all duration-300 ease-in-out transform hover:-translate-y-0.5 hover:scale-105",
                colorClasses[color],
                sizeClasses[size],
                rest.className,
                rest.disabled && "opacity-50 cursor-not-allowed",
            )}
            {...rest}
        >
            {children}
        </button>
    );
}

export type TabButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
    active?: boolean;
    children: React.ReactNode;
};

export function TabButton({
    active = false,
    children,
    ...rest
}: TabButtonProps) {
    return (
        <button
            type="button"
            className={clsx(
                tabToggleBaseClasses,
                active
                    ? tabToggleStateClasses.active
                    : tabToggleStateClasses.inactive,
                rest.className,
                rest.disabled && "opacity-50 cursor-not-allowed",
            )}
            {...rest}
        >
            {children}
        </button>
    );
}