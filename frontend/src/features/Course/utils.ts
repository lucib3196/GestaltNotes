import type { CourseNote } from "../../services/courses";

export function getNoteFormat(note: CourseNote): string {
  const mime = note.content_type?.toLowerCase().split(";")[0].trim();
  if (mime === "application/pdf") return "PDF";
  if (mime === "application/msword") return "DOC";
  if (
    mime ===
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
  )
    return "DOCX";
  if (mime?.startsWith("image/")) return "IMG";
  if (mime?.startsWith("audio/")) return "AUDIO";
  if (mime?.startsWith("video/")) return "VIDEO";
  if (mime?.startsWith("text/")) return "TXT";
  const extension = note.title.match(/\.([a-z0-9]{1,5})$/i)?.[1];
  return extension?.toUpperCase() ?? "FILE";
}