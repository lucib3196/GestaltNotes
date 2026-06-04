import type { FileEntry } from "../models/lecture.types";
import { useState, useMemo, useEffect } from "react";
import { ref, getStorage } from "firebase/storage";
import { listFilesRecursive } from "../utils";
import { getFileName } from "../utils";
import {
    LecturePayloadSchema,
    type ParsedLecture,
} from "../models/lecture.types";
import { getDownloadURL } from "firebase/storage";
import type { PdfSource } from "../models/tool.types";
export function useCourseFiles(path?: string) {
    const [files, setFiles] = useState<FileEntry[]>([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const storage = getStorage();

    const rootRef = useMemo(() => {
        return ref(storage, path);
    }, [path]);

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

    return { files, error, loading };
}

export function useParsedLecture(target?: FileEntry | null) {
    const [lecture, setLecture] = useState<ParsedLecture | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let cancelled = false;
        const loadTarget = async () => {
            if (!target) return;
            if (getFileName(target) !== "output.json") return;

            try {
                const text = await (await fetch(target.url)).text();
                const parsed = JSON.parse(text);
                const lectureParsed = LecturePayloadSchema.parse(parsed);
                setLecture(lectureParsed);
            } catch (e: any) {
                if (!cancelled) setError(e.message ?? "Failed to load lecture files");
            } finally {
                if (!cancelled) setLoading(false);
            }
        };
        loadTarget();
        return () => {
            cancelled = true;
        };
    }, [target]);

    return { lecture, loading, error };
}


// Loads up pdf array
export function useLoadPdfs(pdfPaths: string[]) {
    const [sources, setSources] = useState<PdfSource[]>([])
    const [selectedPDF, setSelectedPDF] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<any | null>(null)
    useEffect(() => {
        async function loadPdfs() {
            if (!pdfPaths.length) { setSelectedPDF(null); return; }

            setLoading(true)
            setError(null)

            try {
                const storage = getStorage()
                const resolved = await Promise.all(
                    pdfPaths.map(async (path, index) => {
                        const storageRef = ref(storage, path);
                        const url = await getDownloadURL(storageRef);
                        return {
                            id: `${index}-${path}`,
                            path,
                            url,
                        } satisfies PdfSource;
                    }),)
                setSources(resolved)
                setSelectedPDF((prev) =>
                    prev && resolved.some((pdf) => pdf.id === prev) ? prev : resolved[0]?.id ?? null,
                );
            } catch (err) {
                let msg = `Failed to resolve PDFs ${err} `
                console.error(msg);
                setSources([]);
                setSelectedPDF(null);
                setError(msg)
            } finally {
                setLoading(false);
            }

            return () => { }
        }
        void loadPdfs();
    }, [pdfPaths]);


    return { sources, selectedPDF, setSelectedPDF, loading, error }
}
