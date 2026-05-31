import { useState, useEffect, } from "react";
import type { FileEntry } from "../models/lecture.types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

import 'katex/dist/katex.min.css';
export function MarkdownFile({ f }: { f: FileEntry }) {
    const [content, setContent] = useState<string>("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const ext = f.path.split(".").pop()?.toLowerCase();
    useEffect(() => {
        let cancelled = false;

        const load = async () => {
            if (ext !== "md") return;
            try {
                const text = await (await fetch(f.url)).text();
                if (!cancelled) setContent(text.replace(/\/n/g, "\n")
                    .replace(/\\n/g, "\n")
                    .replace(/\n{3,}/g, "\n\n")
                    .trim());
            } catch (e: any) {
                if (!cancelled) setError(e.message ?? "Failed to load markdown");
            } finally {
                if (!cancelled) setLoading(false);
            }
        };

        load();
        return () => {
            cancelled = true;
        };
    }, [ext, f.url]);

    if (ext !== "md") return null;
    if (loading) {
        return (
            <div className="rounded-lg border border-border bg-surface p-6 text-sm text-text-muted">
                Loading markdown...
            </div>
        );
    }
    if (error) {
        return (
            <div className="rounded-lg border border-red-400/40 bg-red-500/10 p-6 text-sm text-red-200">
                {error}
            </div>
        );
    }

    console.log("Formatted content", content)

    return (
        <article className="rounded-lg border border-border bg-surface-strong p-6 shadow-soft">
            <div className="documentation-markdown container text-text">
                <ReactMarkdown rehypePlugins={[rehypeKatex]} remarkPlugins={[remarkGfm, remarkMath]}>{content}</ReactMarkdown>
            </div>
        </article>
    );
}
