import api from "../../config/api";
import { noteBlockSchema } from "./schemas";

export async function fetchNoteBlocks(
  token: string,
  courseId: string,
  fileId: string,
  signal?: AbortSignal,
) {
  const response = await api.get<unknown>(
    `/courses/${encodeURIComponent(courseId)}/blocks`,
    {
      params: { source_file_id: fileId },
      headers: { Authorization: `Bearer ${token}` },
      signal,
    },
  );

  return noteBlockSchema.array().parse(response.data);
}
