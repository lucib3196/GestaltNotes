import { useNavigate, useParams } from "react-router-dom";
import { CourseResources } from "../Course/components/CourseResources";
import { useGetCourse } from "./hooks";

import CourseHeader from "../Course/components/CourseHeader";

export default function SingleCourse() {
  const navigate = useNavigate();
  const { courseId } = useParams();
  const { course, refetch } = useGetCourse(courseId);

  if (!course) {
    return;
  }

  return (
    <div className="flex w-full  flex-col gap-6 px-4 py-8 sm:px-6 lg:px-8">
      <button
        type="button"
        onClick={() => navigate("/educator/courses")}
        className="w-fit rounded-lg border border-border bg-surface px-4 py-2 text-sm font-semibold text-text transition-colors hover:bg-surface-muted"
      >
        Back to courses
      </button>
      <CourseHeader course={course} refetch={refetch} />
      <CourseResources courseId={course.id} />
    </div>
  );
}
