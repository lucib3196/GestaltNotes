import { useEffect, useState } from "react";
import { updateEmail, updatePassword } from "firebase/auth";
import { FaEdit } from "react-icons/fa";
import { toast } from "react-toastify";
import clsx from "clsx";

import { useAuth } from "../../Auth";
import { FieldRow, ProfileAvatar, RoleSummary } from ".";

const inputClassName =
  "w-full rounded-lg border border-border bg-surface-strong px-3 py-2 text-sm text-text outline-none transition-colors focus:border-accent disabled:opacity-70";

export default function AccountProfile() {
  const { user, userData } = useAuth();

  const [editMode, setEditMode] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    if (!userData) return;
    setUsername(userData.username ?? "");
    setEmail(userData.email ?? "");
  }, [userData]);

  const handleSave = async () => {
    if (!user || !userData) return;

    try {
      if (email !== userData.email) {
        await updateEmail(user, email);
      }

      if (password.trim().length > 0) {
        await updatePassword(user, password);
      }

      setPassword("");
      setEditMode(false);
      toast.success("Account updated successfully.");
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Could not update account.";
      toast.error(message);
    }
  };

  if (!userData) return null;

  return (
    <section className="overflow-hidden rounded-xl border border-border bg-surface shadow-soft">
      <div className="border-b border-border bg-surface-strong px-5 py-5 sm:px-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-4">
            <ProfileAvatar
              firstName={userData.first_name}
              lastName={userData.last_name}
              src={null}
            />
            <div>
              <h2 className="text-lg font-semibold text-text">
                Profile details
              </h2>
              <p className="mt-1 text-sm text-text-muted">{userData.email}</p>
            </div>
          </div>

          <button
            type="button"
            onClick={() => setEditMode((prev) => !prev)}
            disabled
            className={clsx(
              "inline-flex w-fit items-center gap-2 rounded-md border border-border px-3 py-2 text-sm font-medium text-text-muted",
              "cursor-not-allowed bg-button-secondary opacity-70",
            )}
          >
            <FaEdit className="h-3.5 w-3.5" />
            {editMode ? "Cancel" : "Edit"}
          </button>
        </div>
      </div>

      <div className="grid gap-6 p-5 sm:p-6 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.2fr)]">
        <aside className="rounded-lg border border-border bg-surface-muted p-4">
          <h3 className="text-sm font-semibold text-text">Access level</h3>
          <p className="mt-1 text-sm leading-6 text-text-muted">
            Your role controls which course and account tools are available.
          </p>
          <div className="mt-4">
            <RoleSummary roles={userData.roles} />
          </div>
        </aside>

        <div className="space-y-4">
          <FieldRow label="First Name">
            <p className="text-sm text-text">{userData.first_name}</p>
          </FieldRow>

          <FieldRow label="Last Name">
            <p className="text-sm text-text">{userData.last_name}</p>
          </FieldRow>

          <FieldRow label="Username">
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={!editMode}
              className={inputClassName}
            />
          </FieldRow>

          <FieldRow label="Email">
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={!editMode}
              className={inputClassName}
            />
          </FieldRow>

          {editMode && (
            <FieldRow label="New Password">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={!editMode}
                placeholder="Leave empty to keep current password"
                className={`${inputClassName} placeholder:text-text-soft`}
              />
            </FieldRow>
          )}

          {editMode && (
            <div className="pt-2 sm:pl-[140px]">
              <button
                type="button"
                onClick={handleSave}
                className="rounded-lg bg-accent px-4 py-2.5 text-sm font-semibold text-bg transition-colors hover:bg-accent-strong"
              >
                Save Changes
              </button>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
