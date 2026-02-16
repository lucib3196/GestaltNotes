import {
    type ButtonColor,
    type ButtonSize,
    colorClasses,
    sizeClasses,
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
