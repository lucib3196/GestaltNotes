import { useState, useEffect } from "react";
import { useAuth } from "../context";
import { type LectureNote } from "../services/courseManager";
import api from "../config/api";

export function useNotes(courseId: string | undefined) {
    const [notes, setNotes] = useState<LectureNote[]>([]);
    const [uploading, setUploading] = useState(false);
    const { getIdToken } = useAuth();

    async function fetchNotes() {
        if (!courseId) return;
        try {
            const token = await getIdToken();
            const res = await api.get(`/notes/${courseId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setNotes(res.data.map((n: any) => ({
                id: n.id,
                title: n.title,
                fileName: n.file_name,
                fileUrl: n.file_url,
                uploadedAt: n.uploaded_at,
                sizeKb: 0,
            })));
        } catch (e) {
            console.error("Failed to fetch notes", e);
        }
    }

    useEffect(() => {
        fetchNotes();
    }, [courseId]);

    async function handleFiles(files: FileList | null) {
        if (!files || files.length === 0 || !courseId) return;
        setUploading(true);
        try {
            const token = await getIdToken();
            for (const file of Array.from(files)) {
                const formData = new FormData();
                formData.append("file", file);
                await api.post(`/notes/${courseId}`, formData, {
                    headers: { Authorization: `Bearer ${token}` },
                });
            }
            await fetchNotes(); // re-fetch instead of manually pushing
        } catch (e) {
            console.error("Failed to upload notes", e);
        } finally {
            setUploading(false);
        }
    }

    async function handleDelete(id: string) {
        try {
            const token = await getIdToken();
            await api.delete(`/notes/${courseId}/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setNotes((prev) => prev.filter((n) => n.id !== id));
        } catch (e) {
            console.error("Failed to delete note", e);
        }
    }

    return { notes, uploading, handleFiles, handleDelete };
}