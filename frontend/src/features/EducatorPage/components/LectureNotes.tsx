import { type LectureNote, fmtDate, fmtSize } from "../../../services/courseManager";

interface LectureNotesProps {
    notes: LectureNote[];
    uploading: boolean;
    dragging: boolean;
    setDragging: (val: boolean) => void;
    fileRef: React.RefObject<HTMLInputElement | null>;
    handleFiles: (files: FileList | null) => void;
    handleDelete: (id: string) => void;
}

export default function LectureNotes({ notes, uploading, dragging, setDragging, fileRef, handleFiles, handleDelete }: LectureNotesProps) {
    return (
        <div>
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
    );
}