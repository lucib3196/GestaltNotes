import { DocumentTextIcon } from "@heroicons/react/24/outline";

export default function FileBox({ file }: { file: File }) {
  const size = file.size >= 1024 * 1024
    ? `${(file.size / (1024 * 1024)).toFixed(1)} MB`
    : `${(file.size / 1024).toFixed(1)} KB`;
  return (
    <div className="flex min-w-0 items-center gap-4">
      <div className="flex h-14 w-12 shrink-0 items-center justify-center rounded-lg border border-border bg-surface-muted">
        <DocumentTextIcon aria-hidden="true" className="h-6 w-6 text-text-soft" />
      </div>
      <div className="min-w-0">
        <p title={file.name} className="truncate font-semibold text-text">{file.name}</p>
        <p className="mt-1 text-sm text-text-soft">{size}</p>
      </div>
    </div>
  );
}
