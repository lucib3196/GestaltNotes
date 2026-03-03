import { useState } from "react";
import clsx from "clsx";
import { MessageStyle, MessageBaseStyle } from "./config";
interface Source {
    metadata?: {
        source_pdf?: string;
    };
}

interface SourcesSectionProps {
    sources: Source[];
}

export default function SourceSection({ sources }: SourcesSectionProps) {
    const [open, setOpen] = useState(false);

    const uniqueSources = Array.from(
        new Set(sources.map((s) => s.metadata?.source_pdf).filter(Boolean)),
    );

    if (uniqueSources.length === 0) return null;
    return (
        <div
            key={"sources"}
            className={clsx(
                MessageStyle["ai"],
                MessageBaseStyle,
                "w-full"
            )}
        >
            <button
                onClick={() => setOpen((prev) => !prev)}
                className="text-blue-600 hover:text-blue-800 font-medium flex items-center gap-2"
            >
                {open ? "▼" : "▶"} Sources ({uniqueSources.length})
            </button>
            {open && (
                <div className="mt-2 pl-4 border-l border-slate-300 space-y-1">
                    {uniqueSources.map((src) => (
                        <a
                            key={src}
                            href={`/${src}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="block text-slate-600 hover:text-blue-600 underline"
                        >
                            {src ?? "".split("/").pop()}
                        </a>
                    ))}
                </div>
            )}
        </div>)
}
