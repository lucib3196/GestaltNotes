export default function UploadButton<TItem>({
  items,
  handleUpload,
  uploading,
  disabled = false,
}: {
  items: TItem[];
  handleUpload: () => Promise<void>;
  uploading: boolean;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      disabled={disabled || items.length === 0 || uploading}
      onClick={handleUpload}
      className="w-fit rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-bg disabled:cursor-not-allowed disabled:opacity-60"
    >
      {uploading ? "Uploading..." : "Upload files"}
    </button>
  );
}
