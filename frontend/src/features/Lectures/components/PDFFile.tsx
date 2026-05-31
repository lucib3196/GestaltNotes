import type { FileEntry } from "../models/lecture.types";
import { getFileName } from "../utils";
export default function PDFFile({ file }: { file: FileEntry }) {
    const filename = getFileName(file)
    return (
        <section className="rounded-lg border border-border bg-surface-strong p-4 shadow-soft">
            <header className="mb-3 border-b border-border pb-2">
                <h3 className="truncate text-sm font-medium text-text">{filename}</h3>
            </header>
            <div className="overflow-hidden rounded-md border border-border-strong bg-surface">
                <iframe
                    src={file.url}
                    title={filename}
                    width="100%"
                    height={700}
                    style={{ border: "none" }}
                />
            </div>
        </section>
    )
}
