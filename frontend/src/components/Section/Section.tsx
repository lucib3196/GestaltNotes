import clsx from "clsx";

export const SectionBaseStyle =
    "w-full px-6 py-16 md:px-10 md:py-24";


type SectionVariant = "primary" | "hero";
export const SectionStyle: Record<SectionVariant, string> = {
    primary: `
    bg-white
    text-slate-900
  `,

    hero: `
    bg-gradient-to-b from-slate-50 to-white
    text-slate-900
  `,
};
export type SectionProps = React.HTMLAttributes<HTMLDivElement> & {
    children: React.ReactNode;
    variant?: SectionVariant;
};

export default function Section({
    children,
    variant = "primary",
    ...rest
}: SectionProps) {
    return (
        <section className={clsx(SectionStyle[variant], SectionBaseStyle, rest.className)} {...rest}>
            {children}
        </section>
    );
}
