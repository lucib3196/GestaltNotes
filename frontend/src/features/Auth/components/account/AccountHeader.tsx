type AccountHeaderProps = {
  title?: string;
  subtitle?: string;
};

export default function AccountHeader({
  title = "My Account",
  subtitle = "View and manage your account details",
}: AccountHeaderProps) {
  return (
    <header className="flex flex-col gap-1">
      <h1 className="text-3xl font-bold tracking-tight text-text">{title}</h1>
      <p className="text-sm text-text-muted">{subtitle}</p>
    </header>
  );
}
