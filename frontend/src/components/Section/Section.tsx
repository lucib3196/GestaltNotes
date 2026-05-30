import clsx from "clsx";

export const SectionBaseStyle = clsx(
  "relative w-full px-6 py-16 md:px-10 md:py-24",
  "text-text",
);

type SectionVariant = "primary" | "hero" | "muted" | "elevated" | "accent";
export const SectionStyle: Record<SectionVariant, string> = {
  primary: clsx(
    "bg-surface",
    "border-y border-border/70",
  ),

  hero: clsx(
    "overflow-hidden",
    "bg-[var(--bg-accent)]",
    "border-y border-border",
    "shadow-soft",
  ),

  muted: clsx(
    "bg-surface-muted",
    "border-y border-border/60",
  ),

  elevated: clsx(
    "rounded-xl border border-border bg-surface-strong shadow-soft backdrop-blur",
    "md:mx-auto md:max-w-6xl",
  ),

  accent: clsx(
    "bg-surface border-y border-accent/35",
    "before:pointer-events-none before:absolute before:inset-0",
    "before:bg-[radial-gradient(circle_at_12%_22%,var(--accent),transparent_28%)]",
    "before:opacity-10",
  ),
};

type SectionSpacing = "compact" | "default" | "comfortable";
const SectionSpacingStyle: Record<SectionSpacing, string> = {
  compact: "py-10 md:py-14",
  default: "py-16 md:py-24",
  comfortable: "py-20 md:py-28",
};

export type SectionProps = React.HTMLAttributes<HTMLDivElement> & {
  children: React.ReactNode;
  variant?: SectionVariant;
  spacing?: SectionSpacing;
  contentClassName?: string;
};

export default function Section({
  children,
  variant = "primary",
  spacing = "default",
  contentClassName,
  ...rest
}: SectionProps) {
  return (
    <section
      className={clsx(
        SectionBaseStyle,
        SectionStyle[variant],
        SectionSpacingStyle[spacing],
        "transition-colors duration-base ease-base",
        rest.className,
      )}
      {...rest}
    >
      <div className={clsx("relative z-10 mx-auto w-full max-w-6xl", contentClassName)}>
        {children}
      </div>
    </section>
  );
}
