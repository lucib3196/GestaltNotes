type FieldRowProps = {
  label: string;
  children: React.ReactNode;
};

export default function FieldRow({ label, children }: FieldRowProps) {
  return (
    <div className="grid grid-cols-1 gap-2 sm:grid-cols-[140px_1fr] sm:items-center">
      <label className="text-sm font-medium text-text-muted">{label}</label>
      {children}
    </div>
  );
}
