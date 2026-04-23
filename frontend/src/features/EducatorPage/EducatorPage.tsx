import { useState, useEffect, useRef } from "react";
import { useAuth } from "../../context";
import UserManager, { type Student } from "../../services/userManager";
import NavBar from "../../components/NavBar/NavBar";
import api from "../../config/api";

// ─── Mock types (replace with your SQLModel API types) ───────────────────────

interface LectureNote {
    id: string;
    title: string;
    fileName: string;
    fileUrl: string;
    uploadedAt: string;
    sizeKb: number;
}

interface Course{
    id: string;
    name: string;
    description: string;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function fmtDate(iso: string) {
    return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function fmtSize(kb: number) {
    return kb >= 1000 ? `${(kb / 1000).toFixed(1)} MB` : `${kb} KB`;
}

// ─── Main Component ───────────────────────────────────────────────────────────

type Tab = "students" | "notes";

export default function EducatorPage() {
    const [tab, setTab] = useState<Tab>("students");
    const [search, setSearch] = useState("");
    const [notes, setNotes] = useState<LectureNote[]>([]);
    const [dragging, setDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const fileRef = useRef<HTMLInputElement>(null);
    const [students, setStudents] = useState<Student[]>([]);
    const [course, setCourse] = useState<Course | null>(null);
    const { getIdToken } = useAuth();

    useEffect(() => {
        async function fetchData() {
            const token = await getIdToken();
            const headers = { Authorization: `Bearer ${token}` };
            try {
                const [studentsData, coursesData] = await Promise.all([
                    UserManager.getStudents(token!),
                    api.get("/courses/get_prof_courses", { headers }).then((r) => r.data),
                ]);
                setStudents(studentsData);
                setCourse(coursesData[0] ?? null);
            } catch (e) {
                console.error("Failed to fetch educator data", e);
            }
        }
        fetchData();
    }, []);

    async function handleFiles(files: FileList | null) {
        if (!files || files.length === 0 || !course?.id) return;
        setUploading(true);
        try {
            const token = await getIdToken();
            const newNotes: LectureNote[] = [];
            for (const file of Array.from(files)) {
                const formData = new FormData();
                formData.append("file", file);
                const res = await api.post(`/notes/${course.id}`, formData, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                newNotes.push({
                    id: res.data.id,
                    title: res.data.title,
                    fileName: res.data.file_name,
                    fileUrl: res.data.file_url,
                    uploadedAt: res.data.uploaded_at,
                    sizeKb: Math.round(file.size / 1024),
                });
            }
            setNotes((prev) => [...newNotes, ...prev]);
        } catch (e) {
            console.error("Failed to upload notes", e);
        } finally {
            setUploading(false);
        }
    }

    const filteredStudents = students.filter(
    (s) =>
        [s.first_name, s.last_name].filter(Boolean).join(" ").toLowerCase().includes(search.toLowerCase()) ||
        s.email.toLowerCase().includes(search.toLowerCase())
    );

    async function handleDelete(id: string) {
        try {
            const token = await getIdToken();
            await api.delete(`/notes/${course?.id}/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setNotes((prev) => prev.filter((n) => n.id !== id));
        } catch (e) {
            console.error("Failed to delete note", e);
        }
    }

    return (
        <>
        <NavBar />
        <div style={{ minHeight: "100vh", background: "#f9f7f4", fontFamily: "'Georgia', serif" }}>
            {/* ── Header ── */}
            <header style={{ background: "#fff", padding: "1rem 2.5rem 0" }}>
                <h1 style={{ fontSize: 26, fontWeight: 400, margin: "0 0 6px", letterSpacing: "-0.01em" }}>
                    {course?.name ?? "No course assigned"}
                </h1>
                <p style={{ fontSize: 12, letterSpacing: "0.12em", color: "#a8a29e", textTransform: "uppercase", margin: "0", fontFamily: "system-ui, sans-serif" }}>
                    {course?.description ?? "-"}
                </p>
            </header>

            {/* ── Tabs ── */}
            <div style={{ borderBottom: "1px solid #e7e5e4", background: "#fff", paddingLeft: "2.5rem", display: "flex", gap: 0 }}>
                {(["students", "notes"] as Tab[]).map((t) => (
                    <button
                        key={t}
                        onClick={() => setTab(t)}
                        style={{
                            border: "none", background: "none", padding: "14px 20px",
                            fontSize: 14, fontFamily: "system-ui, sans-serif", cursor: "pointer",
                            color: tab === t ? "#1c1917" : "#78716c",
                            borderBottom: tab === t ? "2px solid #1c1917" : "2px solid transparent",
                            marginBottom: -1, fontWeight: tab === t ? 500 : 400,
                            transition: "all 0.15s",
                        }}
                    >
                        {t === "students" ? "Students" : "Lecture Notes"}
                    </button>
                ))}
            </div>

            {/* ── Content ── */}
            <main style={{ maxWidth: 960, margin: "0 auto", padding: "2rem 2rem" }}>

                {/* ── Students Tab ── */}
                {tab === "students" && (
                    <div>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.25rem" }}>
                            <input
                                type="text"
                                placeholder="Search students..."
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                                style={{
                                    width: 260, padding: "8px 14px", borderRadius: 8,
                                    border: "1px solid #e7e5e4", fontSize: 14,
                                    fontFamily: "system-ui, sans-serif", outline: "none",
                                    background: "#fff", color: "#1c1917",
                                }}
                            />
                            <span style={{ fontSize: 13, color: "#78716c", fontFamily: "system-ui, sans-serif" }}>
                                {filteredStudents.length} student{filteredStudents.length !== 1 ? "s" : ""}
                            </span>
                        </div>

                        <div style={{ background: "#fff", borderRadius: 12, border: "1px solid #e7e5e4", overflow: "hidden" }}>
                            {/* Table header */}
                            <div style={{ display: "grid", gridTemplateColumns: "2fr 2.5fr 1.5fr 1.5fr", gap: 0, padding: "10px 20px", background: "#f5f5f4", borderBottom: "1px solid #e7e5e4" }}>
                                {["Name", "Email"].map((h) => (
                                    <span key={h} style={{ fontSize: 11, fontFamily: "system-ui, sans-serif", textTransform: "uppercase", letterSpacing: "0.08em", color: "#78716c", fontWeight: 500 }}>
                                        {h}
                                    </span>
                                ))}
                            </div>

                            {filteredStudents.length === 0 ? (
                                <p style={{ padding: "2rem", textAlign: "center", color: "#a8a29e", fontFamily: "system-ui, sans-serif", fontSize: 14 }}>
                                    No students match your search.
                                </p>
                            ) : (
                                filteredStudents.map((s, i) => (
                                    <div
                                        key={s.id}
                                        style={{
                                            display: "grid", gridTemplateColumns: "2fr 2.5fr 1.5fr 1.5fr",
                                            gap: 0, padding: "14px 20px", alignItems: "center",
                                            borderBottom: i < filteredStudents.length - 1 ? "1px solid #f5f5f4" : "none",
                                            transition: "background 0.1s",
                                        }}
                                        onMouseEnter={(e) => (e.currentTarget.style.background = "#fafaf9")}
                                        onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
                                    >
                                        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                                            <div style={{
                                                width: 32, height: 32, borderRadius: "50%", background: "#292524",
                                                display: "flex", alignItems: "center", justifyContent: "center",
                                                fontSize: 12, color: "#faf9f6", fontFamily: "system-ui, sans-serif", fontWeight: 500, flexShrink: 0,
                                            }}>
                                               {[s.first_name, s.last_name].filter(Boolean).map((n) => n![0]).join("").slice(0, 2)}
                                            </div>
                                            <span style={{ fontSize: 14, color: "#1c1917", fontFamily: "system-ui, sans-serif" }}>{[s.first_name, s.last_name].filter(Boolean).join(" ")}</span>
                                        </div>
                                        <span style={{ fontSize: 13, color: "#78716c", fontFamily: "system-ui, sans-serif" }}>{s.email}</span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                )}

                {/* ── Lecture Notes Tab ── */}
                {tab === "notes" && (
                    <div>
                        {/* Upload zone */}
                        <div
                            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
                            onDragLeave={() => setDragging(false)}
                            onDrop={(e) => { e.preventDefault(); setDragging(false); handleFiles(e.dataTransfer.files); }}
                            onClick={() => fileRef.current?.click()}
                            style={{
                                border: `2px dashed ${dragging ? "#1c1917" : "#d6d3d1"}`,
                                borderRadius: 12, padding: "2.5rem 2rem",
                                textAlign: "center", cursor: "pointer",
                                background: dragging ? "#f5f5f4" : "#fff",
                                marginBottom: "1.5rem",
                                transition: "all 0.15s",
                            }}
                        >
                            <input
                                ref={fileRef}
                                type="file"
                                accept=".pdf,.ppt,.pptx,.docx"
                                multiple
                                style={{ display: "none" }}
                                onChange={(e) => handleFiles(e.target.files)}
                            />
                            {uploading ? (
                                <p style={{ color: "#78716c", fontSize: 14, fontFamily: "system-ui, sans-serif", margin: 0 }}>Uploading…</p>
                            ) : (
                                <>
                                    <div style={{ fontSize: 28, marginBottom: 10 }}>↑</div>
                                    <p style={{ fontFamily: "system-ui, sans-serif", fontSize: 15, color: "#1c1917", margin: "0 0 4px", fontWeight: 500 }}>
                                        Drop files here or click to upload
                                    </p>
                                    <p style={{ fontFamily: "system-ui, sans-serif", fontSize: 13, color: "#a8a29e", margin: 0 }}>
                                        PDF, PPTX, DOCX supported
                                    </p>
                                </>
                            )}
                        </div>

                        {/* Notes list */}
                        {notes.length === 0 ? (
                            <p style={{ textAlign: "center", color: "#a8a29e", fontFamily: "system-ui, sans-serif", fontSize: 14 }}>
                                No lecture notes uploaded yet.
                            </p>
                        ) : (
                            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                                {notes.map((n) => (
                                    <div
                                        key={n.id}
                                        style={{
                                            background: "#fff", border: "1px solid #e7e5e4", borderRadius: 10,
                                            padding: "14px 18px", display: "flex", alignItems: "center", gap: 14,
                                        }}
                                    >
                                        {/* File icon */}
                                        <div style={{
                                            width: 38, height: 38, borderRadius: 8, background: "#f5f5f4",
                                            display: "flex", alignItems: "center", justifyContent: "center",
                                            fontSize: 11, fontFamily: "system-ui, sans-serif", color: "#78716c",
                                            fontWeight: 600, flexShrink: 0, letterSpacing: "0.03em",
                                        }}>
                                            {n.fileName.split(".").pop()?.toUpperCase()}
                                        </div>

                                        <div style={{ flex: 1, minWidth: 0 }}>
                                            <p style={{ margin: "0 0 2px", fontSize: 14, color: "#1c1917", fontFamily: "system-ui, sans-serif", fontWeight: 500, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                                                {n.title}
                                            </p>
                                            <p style={{ margin: 0, fontSize: 12, color: "#a8a29e", fontFamily: "system-ui, sans-serif" }}>
                                                {n.fileName} · {fmtSize(n.sizeKb)} · Uploaded {fmtDate(n.uploadedAt)}
                                            </p>
                                        </div>

                                        <button
                                            onClick={() => handleDelete(n.id)}
                                            style={{
                                                border: "none", background: "none", cursor: "pointer",
                                                color: "#a8a29e", fontSize: 18, padding: "4px 8px",
                                                borderRadius: 6, lineHeight: 1, flexShrink: 0,
                                                transition: "color 0.1s",
                                            }}
                                            title="Delete note"
                                            onMouseEnter={(e) => (e.currentTarget.style.color = "#dc2626")}
                                            onMouseLeave={(e) => (e.currentTarget.style.color = "#a8a29e")}
                                        >
                                            ×
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </main>
        </div>
         </>
    );
}