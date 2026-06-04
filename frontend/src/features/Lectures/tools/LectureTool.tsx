
import type { RenderPreviewProps } from "../../Tools";
import type { HomeworkArtifact, LectureArtifact } from "../models/tool.types";
import { LecturePdfFrame } from "../../Lectures/components/ui/PDFFrame";
import { useEffect, useMemo, useState } from "react";
import { getFileName } from "../utils";
import { useLoadPdfs } from "../../Lectures/hooks/hooks";

type SourcePdfArtifact = {
  metadata: {
    source_pdf?: string;
  };
};

type SourcePdfPreviewProps<TArtifact extends SourcePdfArtifact> =
  RenderPreviewProps<TArtifact[]> & {
    title: string;
    description: string;
    emptyMessage: string;
    getGroupLabel: (artifact: TArtifact) => string;
  };

function SourcePdfPreview<TArtifact extends SourcePdfArtifact>({
  payload,
  title,
  description,
  emptyMessage,
  getGroupLabel,
}: SourcePdfPreviewProps<TArtifact>) {
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null);

  const groups = useMemo(
    () =>
      Array.from(
        new Set(
          payload
            .filter((artifact) => Boolean(artifact.metadata.source_pdf))
            .map(getGroupLabel)
            .filter(Boolean),
        ),
      ),
    [payload, getGroupLabel],
  );

  useEffect(() => {
    setSelectedGroup((prev) =>
      prev && groups.includes(prev) ? prev : (groups[0] ?? null),
    );
  }, [groups]);

  const sourcePdfPaths = useMemo(() => {
    if (!selectedGroup) return [];

    return payload
      .filter(
        (artifact) =>
          getGroupLabel(artifact) === selectedGroup &&
          Boolean(artifact.metadata.source_pdf),
      )
      .map((artifact) => artifact.metadata.source_pdf)
      .filter((path): path is string => Boolean(path));
  }, [payload, selectedGroup, getGroupLabel]);

  const { sources, selectedPDF, loading } = useLoadPdfs(sourcePdfPaths);

  const selectedPdf = sources.find((pdf) => pdf.id === selectedPDF) ?? null;

  if (loading) {
    return (
      <div className="rounded-lg border border-border bg-surface p-4 text-sm text-text-muted">
        Loading source PDFs...
      </div>
    );
  }

  if (!selectedPdf) {
    return (
      <div className="rounded-lg border border-border bg-surface p-4 text-sm text-text-muted">
        {emptyMessage}
      </div>
    );
  }

  return (
    <section className="h-full space-y-4 rounded-xl border border-border bg-surface-strong p-4 shadow-soft">
      <div className="space-y-1">
        <h4 className="text-sm font-semibold text-text">{title}</h4>
        <p className="text-xs text-text-muted">{description}</p>
      </div>

      <div className="flex flex-wrap gap-2">
        {groups.map((group) => (
          <button
            key={group}
            type="button"
            onClick={() => setSelectedGroup(group)}
            className={`rounded-md border px-3 py-1.5 text-xs font-medium transition-all duration-base ease-base focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 ${selectedGroup === group
              ? "border-border-strong bg-surface text-text shadow-soft"
              : "border-border bg-surface-strong text-text-muted hover:bg-surface-muted hover:text-text"
              }`}
          >
            {group}
          </button>
        ))}
      </div>

      <LecturePdfFrame src={selectedPdf.url} />
    </section>
  );
}

export function LecturePreview(props: RenderPreviewProps<LectureArtifact[]>) {
  return (
    <SourcePdfPreview
      {...props}
      title="Source PDFs"
      description="These are the source PDFs for the retrieved lecture content. Review them for further clarification."
      emptyMessage="No source PDFs found."
      getGroupLabel={(artifact) => artifact.metadata.lecture_title}
    />
  );
}

export function HomeworkPreview(props: RenderPreviewProps<HomeworkArtifact[]>) {
  return (
    <SourcePdfPreview
      {...props}
      title="Homework PDFs"
      description="These are the source PDFs for the retrieved homework content. Review them for further clarification."
      emptyMessage="No homework PDFs found."
      getGroupLabel={(artifact) => {
        return [
          `HW-${artifact.metadata.homework}`,
          artifact.metadata.source_pdf?.split("/").at(-1),
        ]
          .filter(Boolean)
          .join(" - ") || "Unknown source";
      }}
    />
  );
}
