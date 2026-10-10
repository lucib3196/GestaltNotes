import clsx from "clsx";

type PDFViewerProps = {
  src: string;
  title?: string;
  className?: string;
};

export function PDFViewer({ src, title = "PDF document", className }: PDFViewerProps) {
  return (
    <div className={clsx("w-full min-w-0 overflow-hidden bg-surface-strong", className ?? "h-125 rounded-lg border border-border")}>
      <iframe src={src} title={title} loading="lazy" className="h-full w-full border-0" />
    </div>
  );
}
