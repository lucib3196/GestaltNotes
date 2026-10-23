import { useEffect, useRef, useState } from "react";
import { FiPlus } from "react-icons/fi";
import {
  useDeleteCourseNote,
  useDownloadCourseNotes,
  useFetchCourseNotes,
  useStreamCourseNote,
  useUpdateCourseNote,
} from "../../../hooks/courses";
import type { CourseContentType, CourseNote } from "../../../services/courses";
import Modal from "../../../components/Modal/Modal";
import CourseNoteUpload from "../../CourseNote/components/CourseNoteUpload";
import { CourseNoteBox } from "./CourseNoteBox";
import { ResourceActions } from "./ResourceActions";
import { ResourcePreview } from "./ResourcePreview";
import { useCourseDetailsStore } from "../instance";

export default function CourseMaterials() {
  const courseId = useCourseDetailsStore((state) => state.selectedCourseId);
  const {
    notes,
    setNotes,
    loading: fetching,
    error: fetchError,
    refetch,
  } = useFetchCourseNotes(courseId);


  console.log("Materials", notes)
  return <div>Materials</div>;
}
