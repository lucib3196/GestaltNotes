import { useEffect, useState } from "react";



type PreviewKind = "pdf" | "image" | "audio" | "video" | "text" | "other";

type Preview = {
  file: File;
  url: string;
  kind: PreviewKind;
  text: string | null;
  truncated: boolean;
  error: string | null;
};

const TEXT_PREVIEW_LIMIT = 100 * 1024; // 100 KB


type PreviewProps = {
    file: File
    showDownload?:boolean
}

function getPreviewKind(file: File): PreviewKind {
  const extension = file.name.split(".").pop()?.toLowerCase() ?? "";
  const mime = file.type.toLowerCase();

  if (mime === "application/pdf" || extension === "pdf") return "pdf";

  // Display markup and code as plain text.
  if (
    mime.startsWith("text/") ||
    /(?:json|xml|yaml|javascript)/.test(mime) ||
    [
      "txt", "md", "mdx", "csv", "tsv", "json", "xml", "yaml", "yml",
      "html", "htm", "svg", "css", "js", "jsx", "ts", "tsx",
      "py", "java", "c", "cpp", "h", "sql", "log",
    ].includes(extension)
  ) {
    return "text";
  }

  if (
    mime.startsWith("image/") ||
    ["png", "jpg", "jpeg", "gif", "webp", "avif", "bmp"].includes(extension)
  ) {
    return "image";
  }

  if (
    mime.startsWith("audio/") ||
    ["mp3", "wav", "ogg", "m4a", "aac", "flac"].includes(extension)
  ) {
    return "audio";
  }

  if (
    mime.startsWith("video/") ||
    ["mp4", "webm", "mov", "mkv", "ogv"].includes(extension)
  ) {
    return "video";
  }

  return "other";
}

export default function FilePreview({ file, showDownload=false }: PreviewProps) {
  const [preview, setPreview] = useState<Preview | null>(null);

  useEffect(() => {
    let cancelled = false;
    const kind = getPreviewKind(file);

    // Some files arrive without a PDF MIME type.
    const source =
      kind === "pdf"
        ? file.slice(0, file.size, "application/pdf")
        : file;

    const url = URL.createObjectURL(source);

    setPreview({
      file,
      url,
      kind,
      text: null,
      truncated: file.size > TEXT_PREVIEW_LIMIT,
      error: null,
    });

    if (kind === "text") {
      file
        .slice(0, TEXT_PREVIEW_LIMIT)
        .text()
        .then((text) => {
          if (cancelled) return;

          setPreview((current) =>
            current?.file === file ? { ...current, text } : current,
          );
        })
        .catch(() => {
          if (cancelled) return;

          setPreview((current) =>
            current?.file === file
              ? { ...current, error: "Could not read this file." }
              : current,
          );
        });
    }

    return () => {
      cancelled = true;
      URL.revokeObjectURL(url);
    };
  }, [file]);

  // Avoid showing the previous file while the new effect runs.
  if (!preview || preview.file !== file) {
    return (
      <p className="mt-3 text-sm text-text-soft" role="status">
        Preparing preview…
      </p>
    );
  }

  function handlePreviewError() {
    setPreview((current) =>
      current?.file === file
        ? {
            ...current,
            error: "Your browser could not preview this file. Download it to open it.",
          }
        : current,
    );
  }

  return (
    <section
      aria-label={`Preview of ${file.name}`}
      className="mt-3 min-w-0 overflow-hidden rounded-xl border border-border"
    >
      <div className="border-b border-border px-4 py-3">
        <p className="break-all text-sm font-medium">{file.name}</p>
      </div>

      <div className="p-4">
        {preview.error ? (
          <p className="text-sm text-text-soft" role="status">
            {preview.error}
          </p>
        ) : (
          <>
            {preview.kind === "pdf" && (
              <>
                <iframe
                  key={preview.url}
                  src={preview.url}
                  title={`Preview of ${file.name}`}
                  className="h-128 w-full rounded-lg border border-border"
                />
                <p className="mt-2 text-xs text-text-soft">
                  If the PDF doesn’t display, use the download below.
                </p>
              </>
            )}

            {preview.kind === "image" && (
              <img
                key={preview.url}
                src={preview.url}
                alt={`Preview of ${file.name}`}
                onError={handlePreviewError}
                className="mx-auto max-h-96 max-w-full rounded-lg object-contain"
              />
            )}

            {preview.kind === "audio" && (
              <audio
                key={preview.url}
                src={preview.url}
                controls
                preload="metadata"
                aria-label={`Listen to ${file.name}`}
                onError={handlePreviewError}
                className="w-full"
              />
            )}

            {preview.kind === "video" && (
              <video
                key={preview.url}
                src={preview.url}
                controls
                playsInline
                preload="metadata"
                aria-label={`Watch ${file.name}`}
                onError={handlePreviewError}
                className="max-h-96 w-full rounded-lg"
              />
            )}

            {preview.kind === "text" && (
              <>
                {preview.text === null ? (
                  <p className="text-sm text-text-soft" role="status">
                    Reading file…
                  </p>
                ) : (
                  <pre className="max-h-96 overflow-auto whitespace-pre-wrap break-words rounded-lg bg-surface-muted p-4 text-sm">
                    <code>{preview.text || "(Empty file)"}</code>
                  </pre>
                )}

                {preview.truncated && (
                  <p className="mt-2 text-xs text-text-soft">
                    Showing the first 100 KB. Download for the full content.
                  </p>
                )}
              </>
            )}

            {preview.kind === "other" && (
              <p className="text-sm text-text-soft">
                Preview isn’t available for this format. Download the file
                to open it.
              </p>
            )}
          </>
        )}
      </div>

      {showDownload && <div className="border-t border-border px-4 py-3">
        <a
          href={preview.url}
          download={file.name}
          className="text-sm text-accent underline underline-offset-4"
        >
          Download file
        </a>
      </div>}
    </section>
  );
}
