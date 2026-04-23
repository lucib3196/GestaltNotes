export type Tab = "students" | "notes";

interface EducatorTabsProps {
    tab: Tab;
    setTab: (t: Tab) => void;
}

export default function EducatorTabs({ tab, setTab }: EducatorTabsProps) {
    return (
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
    );
}