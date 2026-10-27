import type { ValidRole } from "../../../services";

const roleDetails: Record<ValidRole, { label: string; description: string }> = {
  admin: {
    label: "Admin",
    description:
      "Can help manage platform-level account and support workflows.",
  },
  educator: {
    label: "Educator",
    description:
      "Can manage courses, course materials, and student learning spaces.",
  },
  student: {
    label: "Student",
    description: "Can access enrolled courses, notes, and study tools.",
  },
};

type RoleSummaryProps = {
  roles: ValidRole[];
};

export default function RoleSummary({ roles }: RoleSummaryProps) {
  if (roles.length === 0) {
    return <p className="text-sm text-text-muted">No role assigned yet.</p>;
  }

  return (
    <div className="grid gap-3">
      {roles.map((role) => {
        const detail = roleDetails[role];

        return (
          <article
            key={role}
            className="rounded-lg border border-border bg-surface px-4 py-3"
          >
            <p className="text-sm font-semibold text-text">{detail.label}</p>
            <p className="mt-1 text-sm leading-6 text-text-muted">
              {detail.description}
            </p>
          </article>
        );
      })}
    </div>
  );
}
