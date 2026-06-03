import type { FileEntry } from "../models/lecture.types";
import { useState, useMemo, useEffect } from "react";
import { ref, getStorage } from "firebase/storage";
import { listFilesRecursive } from "../utils";
import { getFileName } from "../utils";
import {
    LecturePayloadSchema,
    type ParsedLecture,
} from "../models/lecture.types";

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
    }, [rootRef])

    return { files, error, loading }
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

            }
            catch (e: any) {
                if (!cancelled) setError(e.message ?? "Failed to load lecture files");
            } finally {
                if (!cancelled) setLoading(false);
            }

        }
        loadTarget()
        return () => {
            cancelled = true;
        };
    }, [target])

    return { lecture, loading, error }
}