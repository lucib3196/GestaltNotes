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
    const [viewMode, setViewMode] = useState<"iframe" | "tab">("iframe");
    const [activeSrc, setActiveSrc] = useState<string | null>(null);

    const uniqueSources = Array.from(
        new Set(sources.map((s) => s.metadata?.source_pdf).filter(Boolean)),
    );

    if (uniqueSources.length === 0) return null;

    return (
        <div
            key="sources"
            className={clsx(
                MessageStyle["ai"],
                MessageBaseStyle,
                "w-full"
            )}
        >
            {/* Header */}
            <div className="flex items-center justify-between">
                <button
                    onClick={() => setOpen((prev) => !prev)}
                    className="text-blue-600 hover:text-blue-800 font-medium flex items-center gap-2"
                >
                    {open ? "▼" : "▶"} Sources ({uniqueSources.length})
                </button>

                {/* View Mode Toggle */}
                <div className="flex gap-2 text-sm">
                    <button
                        onClick={() => setViewMode("iframe")}
                        className={clsx(
                            "px-2 py-1 rounded",
                            viewMode === "iframe"
                                ? "bg-slate-200"
                                : "hover:bg-slate-100"
                        )}
                    >
                        Preview
                    </button>
                    <button
                        onClick={() => setViewMode("tab")}
                        className={clsx(
                            "px-2 py-1 rounded",
                            viewMode === "tab"
                                ? "bg-slate-200"
                                : "hover:bg-slate-100"
                        )}
                    >
                        New Tab
                    </button>
                </div>
            </div>

            {open && (
                <div className="mt-3 pl-4 border-l border-slate-300 space-y-3">
                    {uniqueSources.map((src) => {
                        const filename = src?.split("/").pop();

                        return (
                            <div key={src} className="flex flex-col gap-2">

                                {/* Source Link */}
                                <div className="flex items-center gap-3">
                                    <span className="text-slate-700 text-sm">
                                        {filename}
                                    </span>

                                    {viewMode === "iframe" ? (
                                        <button
                                            onClick={() => setActiveSrc(src ?? "")}
                                            className="text-blue-600 hover:underline text-sm"
                                        >
                                            Preview
                                        </button>
                                    ) : (
                                        <a
                                            href={`/${src}`}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-blue-600 hover:underline text-sm"
                                        >
                                            Open
                                        </a>
                                    )}
                                </div>

                                {/* Inline iframe preview */}
                                {viewMode === "iframe" && activeSrc === src && (
                                    <iframe
                                        src={`/${src}`}
                                        className="w-full h-150 border rounded-lg"
                                    />
                                )}
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}