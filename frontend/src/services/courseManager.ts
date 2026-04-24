import api from "../config/api";

export interface Course {
    id: string;
    name: string;
    description: string;
}

export interface LectureNote {
    id: string;
    title: string;
    fileName: string;
    fileUrl: string;
    uploadedAt: string;
    sizeKb: number;
}

export default class CourseManager {
    private static readonly base = "/courses";

    static async getProfCourses(token: string): Promise<Course[]> {
        const res = await api.get(`${this.base}/get_prof_courses`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return res.data;
    }
}

export function fmtDate(iso: string) {
    return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

export function fmtSize(kb: number) {
    return kb >= 1000 ? `${(kb / 1000).toFixed(1)} MB` : `${kb} KB`;
}