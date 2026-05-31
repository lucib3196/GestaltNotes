import { ref, getStorage } from "firebase/storage";
import { useEffect, useMemo, useState } from "react";
import type { FileEntry } from "../features/Lectures/models/lecture.types";
import { listFilesRecursive, groupByParent } from "../features/Lectures/utils";
import LectureSideBar from "../features/Lectures/components/LectureSideBar";
import { MarkdownFile } from "../features/Lectures/components/MarkdownFile";
import PDFFile from "../features/Lectures/components/PDFFile";
import { getFileExt, getFileName } from "../features/Lectures/utils";
import { GiHamburgerMenu } from "react-icons/gi";

export default function LectureNotes() {
    const [files, setFiles] = useState<FileEntry[]>([]);
    const [selectedFile, setSelectedFile] = useState<FileEntry | null>(null);
    const [sidebarOpen, setSidebarOpen] = useState(true);

    // General loading state
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const storage = getStorage();

    // Get the root storage just the me116 notes for now

    const rootRef = useMemo(() => {
        return ref(storage, "me116_spring_2026/lectures/");
    }, []);

    // Load up the files on entry

    useEffect(() => {
        let cancelled = false;

        const fetchFiles = async () => {
            try {
                setLoading(true);
                const allFiles = await listFilesRecursive(rootRef);
                if (!cancelled) setFiles(allFiles);
            } catch (e: any) {
                if (!cancelled) setError(e.message ?? "Failed to load lecture files");
            } finally {
                if (!cancelled) setLoading(false);
            }
        };
        fetchFiles();
        return () => {
            cancelled = true;
        };
    }, [rootRef]);

    if (loading) return <div>Loading lecture notes...</div>;
    if (error) return <div>Error: {error}</div>;

    // Group files base on parents ex :
    // lecture1->lecture1.pdf, lecture1.md
    // lecture2->lecture2.pdf etc
    const grouped = groupByParent(files);

    return (
        <div className="h-screen bg-bg text-text">
            <div className="flex h-full min-h-0 flex-col">
                <div className="flex items-center justify-between border-b border-border bg-surface/70 px-4 py-3 backdrop-blur-sm">
                    <h1 className="text-sm font-semibold uppercase tracking-wide text-text-muted">Lecture Notes</h1>
                    <button
                        type="button"
                        onClick={() => setSidebarOpen((prev) => !prev)}
                        className="inline-flex items-center gap-2 rounded-md border border-border bg-surface px-3 py-2 text-sm text-text transition-all duration-base ease-base hover:border-border-strong hover:bg-surface-strong"
                    >
                        <GiHamburgerMenu />
                        {sidebarOpen ? "Close Menu" : "Open Menu"}
                    </button>
                </div>

                <div className="flex min-h-0 flex-1">
                    <aside
                        className={`${sidebarOpen ? "w-[320px]" : "w-0"} min-h-0 overflow-hidden border-r border-border bg-surface transition-all duration-base ease-base`}
                    >
                        <div className="h-full overflow-y-auto p-3">
                            <LectureSideBar grouped={grouped} setSelected={setSelectedFile} />
                        </div>
                    </aside>

                    <main className="min-h-0 flex-1 overflow-y-auto p-4 md:p-6">
                        {!selectedFile && (
                            <div className="rounded-lg border border-border bg-surface p-8 text-text-muted">
                                Select a file from the menu to view its content.
                            </div>
                        )}

                        {selectedFile &&
                            (() => {
                                const fileName = getFileName(selectedFile);
                                const ext = getFileExt(selectedFile);

                                switch (ext) {
                                    case "md":
                                        return <MarkdownFile f={selectedFile} />;
                                    case "pdf":
                                        return <PDFFile file={selectedFile} />;
                                    default:
                                        return (
                                            <a href={selectedFile.url} target="_blank" rel="noreferrer">
                                                Open {fileName}
                                            </a>
                                        );
                                }
                            })()}
                    </main>
                </div>
            </div>
        </div>
    );
}
