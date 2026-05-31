import {
  type StorageReference,
  listAll,
  getDownloadURL,
} from "firebase/storage";
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
): Promise<FileEntry[]> {
  const result = await listAll(folderRef);
  const excludedExt = ["json"];
  const filesHere = await Promise.all(
    result.items
      .filter((item) => {
        const name = item.fullPath.split("/").at(-1) ?? "";
        const ext = name.includes(".") ? name.split(".").pop() : "";
        return !excludedExt.includes(ext ?? "");
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
