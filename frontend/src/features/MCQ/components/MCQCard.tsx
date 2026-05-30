

type MCQCardProps = {
    children: React.ReactNode;
};
export default function MCQCard({ children }: MCQCardProps) {
    return (
        <article className="rounded-lg border border-border bg-surface p-4 shadow-soft">
            {children}
        </article>
    );
}