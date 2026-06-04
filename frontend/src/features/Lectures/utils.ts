import {
  type StorageReference,
  listAll,
  getDownloadURL,
} from "firebase/storage";
import { ToolMessage } from "langchain";
import type { LectureArtifact, HomeworkArtifact } from "./models/tool.types";
import type { FileEntry } from "./models/lecture.types";

export function groupByParent(files: FileEntry[]) {
  return files.reduce<Record<string, FileEntry[]>>((acc, file) => {
    const parent = file.parent ?? "";
    if (!acc[parent]) acc[parent] = [];
    acc[parent].push(file);
    return acc;
  }, {});
}

export async function listFilesRecursive(
  folderRef: StorageReference,
  excludedExt?: string[],
): Promise<FileEntry[]> {
  const result = await listAll(folderRef);
  const filesHere = await Promise.all(
    result.items
      .filter((item) => {
        const name = item.fullPath.split("/").at(-1) ?? "";
        const ext = name.includes(".") ? name.split(".").pop() : "";
        return !excludedExt?.includes(ext ?? "");
      })
      .map(async (item) => {
        return {
          path: item.fullPath,
          parent: item.parent?.fullPath,
          url: await getDownloadURL(item),
        };
      }),
  );

  const nestedFilesArrays = await Promise.all(
    result.prefixes.map((subfolderRef) => listFilesRecursive(subfolderRef)),
  );
  return [...filesHere, ...nestedFilesArrays.flat()];
}

export function getFileName(file: FileEntry) {
  return file.path.split("/").at(-1) ?? file.path;
}

export function getFileExt(file: FileEntry) {
  const filename = getFileName(file);
  const ext = filename.includes(".")
    ? filename.split(".").pop()?.toLowerCase()
    : "";
  return ext;
}


function isLectureArtifact(value: unknown): value is LectureArtifact {
  if (!value || typeof value !== "object") return false;

  const v = value as { id?: unknown; metadata?: unknown };
  if (!v.metadata || typeof v.metadata !== "object") return false;

  const m = v.metadata as {
    lecture_title?: unknown;
    source_markdown?: unknown;
    source_pdf?: unknown;
  };

  return (
    typeof m.lecture_title === "string" &&
    (m.source_markdown === undefined ||
      typeof m.source_markdown === "string") &&
    (m.source_pdf === undefined || typeof m.source_pdf === "string")
  );
}
function isHomeworkArtifact(value: unknown): value is HomeworkArtifact {
  if (!value || typeof value !== "object") return false;

  const v = value as { id?: unknown; metadata?: unknown };
  if (!v.metadata || typeof v.metadata !== "object") return false;

  const m = v.metadata as {
    course?: unknown;
    source_markdown?: unknown;
    source_pdf?: unknown;
  };

  return (
    typeof m.course === "string" &&
    (m.source_markdown === undefined ||
      typeof m.source_markdown === "string") &&
    (m.source_pdf === undefined || typeof m.source_pdf === "string")
  );
}

export function parseLectureTool(msg: ToolMessage): LectureArtifact[] {
  const artifacts = Array.isArray(msg.artifact)
    ? msg.artifact.filter(isLectureArtifact)
    : [];

  return artifacts;
}

export function parseHomeworkTool(msg: ToolMessage): HomeworkArtifact[] {
  const artifacts = Array.isArray(msg.artifact)
    ? msg.artifact.filter(isHomeworkArtifact)
    : [];

  return artifacts;
}
