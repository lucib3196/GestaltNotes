import { useState, useEffect } from "react";
import { useAuth } from "../context";
import UserManager, { type Student } from "../services/userManager";
import CourseManager, { type Course } from "../services/courseManager";

export function useEducatorData() {
    const [students, setStudents] = useState<Student[]>([]);
    const [course, setCourse] = useState<Course | null>(null);
    const { getIdToken } = useAuth();

    useEffect(() => {
        async function fetchData() {
            const token = await getIdToken();
            try {
                const [studentsData, coursesData] = await Promise.all([
                    UserManager.getStudents(token!),
                    CourseManager.getProfCourses(token!),
                ]);
                setStudents(studentsData);
                setCourse(coursesData[0] ?? null);
            } catch (e) {
                console.error("Failed to fetch educator data", e);
            }
        }
        fetchData();
    }, []);

    return { students, course };
}