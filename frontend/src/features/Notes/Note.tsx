import { NotesAPI } from "../../services";
import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { MathJax } from "better-react-mathjax";
import { markdownComponents } from "./config";

export default function Note() {
    const [note, setNote] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getNote = async () => {
            try {
                const result = await NotesAPI.getTestNote();

                // setNote(data);
            } finally {
                setLoading(false);
            }
        };

        getNote();
    }, []);

    return (
        <MathJax>
            <div className="min-h-screen bg-gray-50 py-10 px-4">
                <div className="max-w-4xl mx-auto bg-white shadow-sm rounded-lg p-8">

                    {/* Header */}
                    <header className="mb-8 border-b pb-4">
                        <h1 className="text-3xl font-bold tracking-tight">
                            Notes
                        </h1>
                        <p className="text-gray-500 mt-2 text-sm">
                            Lecture content and derivations. Generate summary using AI
                        </p>
                    </header>

                    {/* Content */}
                    {loading ? (
                        <div className="text-gray-400 animate-pulse">
                            Loading notes...
                        </div>
                    ) : (
                        <Markdown
                            remarkPlugins={[remarkGfm]}
                            components={markdownComponents}
                        >
                            {note ?? ""}
                        </Markdown>
                    )}
                </div>
            </div>
        </MathJax>
    );
}
