export function LecturePdfFrame({ src }: { src: string }) {
    return (
        <iframe
            src={`${src}#toolbar=0`}
            className="h-full w-full rounded-md border border-border bg-surface"
        />
    );
}
