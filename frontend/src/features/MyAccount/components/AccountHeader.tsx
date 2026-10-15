type AccountHeaderProps = {
  title?: string;
  subtitle?: string;
};

export default function AccountHeader({
  title = "My Account",
  subtitle = "Review your profile details, account access, and learning workspace role.",
}: AccountHeaderProps) {
  return (
    <header className="flex flex-col gap-2">
      <p className="text-sm font-medium uppercase tracking-[0.18em] text-accent">
        Account
      </p>
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-text sm:text-4xl">{title}</h1>
        <p className="max-w-2xl text-sm leading-6 text-text-muted sm:text-base">
          {subtitle}
        </p>
      </div>
    </header>
  );
}
