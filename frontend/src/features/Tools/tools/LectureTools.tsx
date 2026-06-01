import type { ToolMessage } from "langchain";
import type { RenderPreviewProps } from "../models/tools.types";
import { getDownloadURL } from "firebase/storage";
import { useEffect, useMemo, useState } from "react";
import { getStorage, ref } from "firebase/storage";

type MinimalLecturePayload = {
  lecture_title: string;
  source_markdown?: string;
  source_pdf?: string;
};

type LectureArtifact = {
  id?: string;
  metadata: MinimalLecturePayload;
};

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
    (m.source_markdown === undefined || typeof m.source_markdown === "string") &&
    (m.source_pdf === undefined || typeof m.source_pdf === "string")
  );
}

export function parseLectureTool(msg: ToolMessage): LectureArtifact[] {
  const artifacts = Array.isArray(msg.artifact)
    ? msg.artifact.filter(isLectureArtifact)
    : [];

  return artifacts;
}

type PdfSource = {
  id: string;
  path: string;
  url: string;
};

function LecturePdfFrame({ src }: { src: string }) {
  return (
    <iframe
      src={`${src}#toolbar=0`}
      className="h-full w-full rounded-md border border-border bg-surface"
    />
  );
}

export function LecturePreview({
  payload,
}: RenderPreviewProps<LectureArtifact[]>) {
  const [pdfSources, setPdfSources] = useState<PdfSource[]>([]);
  const [selectedPdfId, setSelectedPdfId] = useState<string | null>(null);
  const [selectedLectureTitle, setSelectedLectureTitle] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const lectureTitles = useMemo(
    () =>
      Array.from(
        new Set(
          payload
            .filter((artifact) => Boolean(artifact.metadata.source_pdf))
            .map((artifact) => artifact.metadata.lecture_title),
        ),
      ),
    [payload],
  );

  useEffect(() => {
    setSelectedLectureTitle((prev) =>
      prev && lectureTitles.includes(prev) ? prev : lectureTitles[0] ?? null,
    );
  }, [lectureTitles]);

  const sourcePdfPaths = useMemo(() => {
    if (!selectedLectureTitle) return [];

    return payload
      .filter(
        (artifact) =>
          artifact.metadata.lecture_title === selectedLectureTitle &&
          Boolean(artifact.metadata.source_pdf),
      )
      .map((artifact) => artifact.metadata.source_pdf)
      .filter((path): path is string => Boolean(path));
  }, [payload, selectedLectureTitle]);

  useEffect(() => {
    async function loadPdfs() {
      if (sourcePdfPaths.length === 0) {
        setPdfSources([]);
        setSelectedPdfId(null);
        return;
      }

      setIsLoading(true);
      try {
        const storage = getStorage();
        const resolved = await Promise.all(
          sourcePdfPaths.map(async (path, index) => {
            const storageRef = ref(storage, path);
            const url = await getDownloadURL(storageRef);
            return {
              id: `${index}-${path}`,
              path,
              url,
            } satisfies PdfSource;
          }),
        );

        setPdfSources(resolved);
        setSelectedPdfId((prev) =>
          prev && resolved.some((pdf) => pdf.id === prev) ? prev : resolved[0]?.id ?? null,
        );
      } catch (err) {
        console.error("Failed to resolve PDFs", err);
        setPdfSources([]);
        setSelectedPdfId(null);
      } finally {
        setIsLoading(false);
      }
    }

    void loadPdfs();
  }, [sourcePdfPaths]);

  const selectedPdf = pdfSources.find((pdf) => pdf.id === selectedPdfId) ?? null;

  if (isLoading) {
    return (
      <div className="rounded-lg border border-border bg-surface p-4 text-sm text-text-muted">
        Loading source PDFs...
      </div>
    );
  }

  if (!selectedPdf) {
    return (
      <div className="rounded-lg border border-border bg-surface p-4 text-sm text-text-muted">
        No source PDFs found.
      </div>
    );
  }

  return (
    <section className="h-full space-y-4 rounded-xl border border-border bg-surface-strong p-4 shadow-soft">
      <div className="space-y-1">
        <h4 className="text-sm font-semibold text-text">Source PDFs</h4>
        <p className="text-xs text-text-muted">
          These are the source PDFs for the retrieved content. Review them for further clarification.
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        {lectureTitles.map((title) => (
          <button
            key={title}
            type="button"
            onClick={() => setSelectedLectureTitle(title)}
            className={`rounded-md border px-3 py-1.5 text-xs font-medium transition-all duration-base ease-base focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 ${selectedLectureTitle === title
              ? "border-border-strong bg-surface text-text shadow-soft"
              : "border-border bg-surface-strong text-text-muted hover:bg-surface-muted hover:text-text"
              }`}
          >
            {title}
          </button>
        ))}
      </div>

      <LecturePdfFrame src={selectedPdf.url} />
    </section>
  );
}
