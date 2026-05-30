import { useState } from "react";
import { toast } from "react-toastify";
import { InputTextForm } from "../../../../components/FormComponents";
import { Button } from "../../../../components/Button";
import { useAuth } from "../../../../context";
import { UserManager } from "../../../../services";

export default function PasswordResetForm() {
    const { user, logout, setMode } = useAuth();
    const [newPassword, setNewPassword] = useState("");
    const [submitting, setSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!user) {
            toast.error("No authenticated user found.");
            return;
        }

        if (!newPassword.trim()) {
            toast.error("Please enter a new password.");
            return;
        }

        try {
            setSubmitting(true);
            const token = await user.getIdToken();
            await UserManager.resetTempPassword(newPassword, token);
            toast.success("Password updated. Please log in again.");
            await logout();
        } catch (error) {
            const message =
                error instanceof Error ? error.message : "Failed to update password";
            toast.error(message);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <section className="w-full max-w-xl rounded-xl border border-border bg-surface p-6 shadow-soft backdrop-blur-md sm:p-7">
            <div className="mb-5 flex flex-col gap-1">
                <h1 className="text-2xl font-semibold tracking-tight text-text">
                    Reset Password
                </h1>
                <p className="text-sm text-text-muted">
                    Set a new password to continue using your account.
                </p>
            </div>

            <form onSubmit={handleSubmit} className="flex w-full flex-col gap-4">
                <InputTextForm
                    variant="auth"
                    value={newPassword}
                    id="new-password"
                    type="password"
                    name="newPassword"
                    label="New Password"
                    placeholder="••••••••"
                    onChange={(e) => setNewPassword(e.target.value)}
                />

                <div className="mt-2 flex flex-col gap-2">
                    <Button
                        type="submit"
                        color="authPrimary"
                        size="md"
                        className="w-full rounded-lg"
                        disabled={submitting}
                    >
                        {submitting ? "Updating..." : "Update Password"}
                    </Button>

                    <Button
                        type="button"
                        color="authGhost"
                        size="md"
                        className="w-full rounded-lg"
                        onClick={() => setMode("login")}
                        disabled={submitting}
                    >
                        Back to Login
                    </Button>
                </div>
            </form>
        </section>
    );
}
