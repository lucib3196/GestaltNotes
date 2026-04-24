import { useState, useRef } from "react";
import NavBar from "../../components/NavBar/NavBar";
import { useEducatorData } from "../../services/useEducatorData";
import { useNotes } from "../../services/useNotes";
import StudentList from "./components/StudentList";
import LectureNotes from "./components/LectureNotes";
import EducatorHeader from "./components/EducatorHeader";
import EducatorTabs, { type Tab } from "./components/EducatorTabs";

export default function EducatorPage() {
    const [tab, setTab] = useState<Tab>("students");
    const [dragging, setDragging] = useState(false);
    const fileRef = useRef<HTMLInputElement>(null);
    const { students, course } = useEducatorData();
    const { notes, uploading, handleFiles, handleDelete } = useNotes(course?.id);

    return (
        <>
            <NavBar />
            <div style={{ minHeight: "100vh", background: "#f9f7f4", fontFamily: "'Georgia', serif" }}>
                <EducatorHeader course={course} />
                <EducatorTabs tab={tab} setTab={setTab} />
                <main style={{ maxWidth: 960, margin: "0 auto", padding: "2rem 2rem" }}>
                    {tab === "students" && <StudentList students={students} />}
                    {tab === "notes" && (
                        <LectureNotes
                            notes={notes}
                            uploading={uploading}
                            dragging={dragging}
                            setDragging={setDragging}
                            fileRef={fileRef}
                            handleFiles={handleFiles}
                            handleDelete={handleDelete}
                        />
                    )}
                </main>
            </div>
        </>
    );
}