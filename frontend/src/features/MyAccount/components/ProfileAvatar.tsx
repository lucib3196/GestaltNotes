type ProfileAvatarProps = {
  firstName?: string;
  lastName?: string;
  src?: string | null;
};

export default function ProfileAvatar({
  firstName,
  lastName,
  src,
}: ProfileAvatarProps) {
  const initials =
    `${firstName?.[0] ?? ""}${lastName?.[0] ?? ""}`.toUpperCase() || "U";

  if (src) {
    return (
      <img
        src={src}
        alt="Profile"
        className="h-20 w-20 rounded-full border border-border object-cover"
      />
    );
  }

  return (
    <div className="flex h-20 w-20 items-center justify-center rounded-full border border-border bg-surface-muted text-xl font-semibold text-text">
      {initials}
    </div>
  );
}
