import { useEffect, useState } from "react";
import { updateEmail, updatePassword } from "firebase/auth";
import { FaEdit } from "react-icons/fa";
import { toast } from "react-toastify";
import { useAuth } from "../../../../context";
import clsx from "clsx";

type FieldRowProps = {
    label: string;
    children: React.ReactNode;
};

function FieldRow({ label, children }: FieldRowProps) {
    return (
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-[140px_1fr] sm:items-center">
            <label className="text-sm font-medium text-text-muted">{label}</label>
            {children}
        </div>
    );
}

type ProfileAvatarProps = {
    firstName?: string;
    lastName?: string;
    src?: string | null;
};

function ProfileAvatar({ firstName, lastName, src }: ProfileAvatarProps) {
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
        <div className="flex h-20 w-20 items-center justify-center rounded-full border border-border bg-surface-strong text-xl font-semibold text-text">
            {initials}
        </div>
    );
}


export default function AccountProfile() {
    const { user, userData } = useAuth();

    console.log(user)

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

            //   if (username !== userData.username || email !== userData.email) {
            //     const updatePayload: UserUpdate = { username, email };
            //     await UserAPI.updateUser(user, updatePayload);
            //   }

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
        <section className="rounded-2xl border border-border bg-surface p-5 shadow-soft backdrop-blur-md">
            <div className="mb-5 flex items-start justify-between gap-4">
                <div className="flex items-center gap-4">
                    <ProfileAvatar
                        firstName={userData.first_name}
                        lastName={userData.last_name}
                        src={null}
                    />
                    <div>
                        <h2 className="text-lg font-semibold text-text">Profile</h2>
                        <p className="text-sm text-text-muted">{userData.email}</p>
                    </div>
                </div>

                <button
                    type="button"
                    onClick={() => setEditMode((prev) => !prev)}
                    disabled={true}
                    className={clsx("inline-flex items-center gap-2 rounded-md px-2 py-1.5 text-sm font-medium text-text-muted transition-colors hover:bg-surface-muted hover:text-text cursor-not-allowed")}
                >
                    <FaEdit className="h-3.5 w-3.5 cursor:cursor:not-allowed" />
                    {editMode ? "Cancel" : "Edit"}
                </button>
            </div>

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
                        className="w-full rounded-lg border border-border bg-surface-strong px-3 py-2 text-sm text-text outline-none transition-colors focus:border-accent disabled:opacity-70"
                    />
                </FieldRow>

                <FieldRow label="Email">
                    <input
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        disabled={!editMode}
                        className="w-full rounded-lg border border-border bg-surface-strong px-3 py-2 text-sm text-text outline-none transition-colors focus:border-accent disabled:opacity-70"
                    />
                </FieldRow>

                {editMode && <FieldRow label="New Password">
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        disabled={!editMode}
                        placeholder="Leave empty to keep current password"
                        className="w-full rounded-lg border border-border bg-surface-strong px-3 py-2 text-sm text-text placeholder:text-text-soft outline-none transition-colors focus:border-accent disabled:opacity-70"
                    />
                </FieldRow>}


            </div>

            {editMode && (
                <div className="mt-6">
                    <button
                        type="button"
                        onClick={handleSave}
                        className="rounded-lg bg-accent px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-accent-strong"
                    >
                        Save Changes
                    </button>
                </div>
            )}
        </section>
    );
}
