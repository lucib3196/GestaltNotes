import { useState, useEffect } from "react";
import { useAuth } from "../context";
import CourseManager, { type Course } from "../services/courseManager";

export interface Student {
    id: string;
    first_name: string | null;
    last_name: string | null;
    email: string;
}

export function useEducatorData() {
    const [students, setStudents] = useState<Student[]>([]);
    const [course, setCourse] = useState<Course | null>(null);
    const { getIdToken } = useAuth();

    useEffect(() => {
        async function fetchData() {
            const token = await getIdToken();
            try {
                const coursesData = await CourseManager.getProfCourses(token!);
                setStudents([]);
                setCourse(coursesData[0] ?? null);
            } catch (e) {
                console.error("Failed to fetch educator data", e);
            }
        }
        fetchData();
    }, []);

    return { students, course };
}
