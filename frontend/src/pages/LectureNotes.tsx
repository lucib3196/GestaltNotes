import { useState } from "react";
import type { FileEntry } from "../features/Lectures/models/lecture.types";
import { groupByParent } from "../features/Lectures/utils";
import LectureSideBar from "../features/Lectures/components/LectureSideBar";
import { MarkdownFile } from "../features/Lectures/components/MarkdownFile";
import PDFFile from "../features/Lectures/components/PDFFile";
import { getFileExt, getFileName } from "../features/Lectures/utils";
import { useCourseFiles } from "../features/Lectures/hooks/hooks";
import LectureJson from "../features/Lectures/components/JsonParser";
import { HomeworkSideBar } from "../features/Lectures/components/LectureSideBar";
const renderSelectedFile = (selectedFile: FileEntry | null) => {
  if (!selectedFile) return null;

  const fileName = getFileName(selectedFile);
  const ext = getFileExt(selectedFile);

  switch (ext) {
    case "md":
      return <MarkdownFile f={selectedFile} />;
    case "pdf":
      return <PDFFile file={selectedFile} />;
    case "json":
      return <LectureJson file={selectedFile} />;
    default:
      return (
        <a href={selectedFile.url} target="_blank" rel="noreferrer">
          Open {fileName}
        </a>
      );
  }
};

export default function LectureNotes() {
  const [selectedFile, setSelectedFile] = useState<FileEntry | null>(null);

  // Get the root storage just the me116 notes for now

  const { files, loading, error } = useCourseFiles("me116_spring_2026/lectures");

  // Load up the files on entry

  if (loading) return <div>Loading lecture notes...</div>;
  if (error) return <div>Error: {error}</div>;

  // Group files base on parents ex :
  // lecture1->lecture1.pdf, lecture1.md
  // lecture2->lecture2.pdf etc
  const grouped = groupByParent(files);

  return (
    <div className="h-screen bg-bg text-text">
      <div className="flex h-full min-h-0 flex-col">
        <div className="flex min-h-0 flex-1">
          <LectureSideBar
            grouped={grouped}
            setSelected={setSelectedFile}
            selected={selectedFile}
          />

          <main className="min-h-0 flex-1 overflow-y-auto p-4 md:p-6">
            {!selectedFile && (
              <div className="rounded-lg border border-border bg-surface p-8 text-text-muted">
                Select a file from the menu to view its content.
              </div>
            )}

            {selectedFile && renderSelectedFile(selectedFile)}
          </main>
        </div>
      </div>
    </div>
  );
}


export function HomeworkNotes() {
  const [selectedFile, setSelectedFile] = useState<FileEntry | null>(null);

  // Get the root storage just the me116 notes for now

  const { files, loading, error } = useCourseFiles("me116_spring_2026/homework");

  

  // Load up the files on entry

  if (loading) return <div>Loading lecture notes...</div>;
  if (error) return <div>Error: {error}</div>;

  // Group files base on parents ex :
  // lecture1->lecture1.pdf, lecture1.md
  // lecture2->lecture2.pdf etc
  const grouped = groupByParent(files);

  return (
    <div className="h-screen bg-bg text-text">
      <div className="flex h-full min-h-0 flex-col">
        <div className="flex min-h-0 flex-1">
          <HomeworkSideBar
            grouped={grouped}
            setSelected={setSelectedFile}
            selected={selectedFile}
          />

          <main className="min-h-0 flex-1 overflow-y-auto p-4 md:p-6">
            {!selectedFile && (
              <div className="rounded-lg border border-border bg-surface p-8 text-text-muted">
                Select a file from the menu to view its content.
              </div>
            )}

            {selectedFile && renderSelectedFile(selectedFile)}
          </main>
        </div>
      </div>
    </div>
  );
}
