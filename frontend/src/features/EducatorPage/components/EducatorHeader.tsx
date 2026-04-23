import { type Course } from "../../../services/courseManager";

interface EducatorHeaderProps {
    course: Course | null;
}

export default function EducatorHeader({ course }: EducatorHeaderProps) {
    return (
        <header style={{ background: "#fff", padding: "1rem 2.5rem 0" }}>
            <h1 style={{ fontSize: 26, fontWeight: 400, margin: "0 0 6px", letterSpacing: "-0.01em" }}>
                {course?.name ?? "No course assigned"}
            </h1>
            <p style={{ fontSize: 12, letterSpacing: "0.12em", color: "#a8a29e", textTransform: "uppercase", margin: "0", fontFamily: "system-ui, sans-serif" }}>
                {course?.description ?? "-"}
            </p>
        </header>
    );
}