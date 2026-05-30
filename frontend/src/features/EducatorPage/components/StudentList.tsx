import { useState } from "react";
import { type Student } from "../../../services/useEducatorData";

interface StudentListProps {
    students: Student[];
}

export default function StudentList({ students }: StudentListProps) {
    const [search, setSearch] = useState("");

    const filteredStudents = students.filter(
        (s) =>
            [s.first_name, s.last_name].filter(Boolean).join(" ").toLowerCase().includes(search.toLowerCase()) ||
            s.email.toLowerCase().includes(search.toLowerCase())
    );

    return (
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
                <div style={{ display: "grid", gridTemplateColumns: "2fr 2.5fr", gap: 0, padding: "10px 20px", background: "#f5f5f4", borderBottom: "1px solid #e7e5e4" }}>
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
                                display: "grid", gridTemplateColumns: "2fr 2.5fr",
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
                                <span style={{ fontSize: 14, color: "#1c1917", fontFamily: "system-ui, sans-serif" }}>
                                    {[s.first_name, s.last_name].filter(Boolean).join(" ")}
                                </span>
                            </div>
                            <span style={{ fontSize: 13, color: "#78716c", fontFamily: "system-ui, sans-serif" }}>{s.email}</span>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
