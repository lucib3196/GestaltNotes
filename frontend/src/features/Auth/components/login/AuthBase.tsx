import { useAuth } from "../../../../context";
import { InputTextForm } from "../../../../components/FormComponents";
import { useState } from "react";
import type { FormEvent } from "react";
import { Button } from "../../../../components/Button";
import { sendPasswordResetEmail, getAuth } from "firebase/auth";
import { toast } from "react-toastify";
import type { AuthMode } from "../../../../context";
import clsx from "clsx";

interface AuthProps {
    onSubmit: (
        email: string,
        password: string,
        username?: string,
        firstName?: string,
        lastName?: string,
    ) => Promise<void>;
}

function AuthHeader({ mode }: { mode: AuthMode }) {
    const isSignup = mode === "signup";
    const isLogin = mode === "login";

    return (
        <div className="mb-5 flex flex-col gap-1">
            <h1 className="text-2xl font-semibold tracking-tight text-text">
                {isLogin ? "Log In" : isSignup ? "Create Account" : "Reset Password"}
            </h1>
            <p className="text-sm text-text-muted">
                {isLogin
                    ? "Welcome back. Sign in to continue."
                    : isSignup
                        ? "Create your account to get started."
                        : "Enter your email to receive a reset link."}
            </p>
        </div>
    );
}

function ModePills({
    mode,
    setMode,
}: {
    mode: AuthMode;
    setMode: (val: AuthMode) => void;
}) {
    return (
        <div className="mb-5">
            <div
                className="inline-flex rounded-full border border-border bg-surface-muted p-1"
                aria-label="Authentication mode switch"
            >
                <button
                    type="button"
                    onClick={() => setMode("login")}
                    className={clsx(
                        "rounded-full px-3 py-1.5 text-sm font-medium transition",
                        mode === "login"
                            ? "bg-surface-strong text-text shadow-sm"
                            : "text-text-muted hover:text-text",
                    )}
                >
                    Log In
                </button>
                <button
                    type="button"
                    onClick={() => setMode("signup")}
                    className={clsx(
                        "rounded-full px-3 py-1.5 text-sm font-medium transition",
                        mode === "signup"
                            ? "bg-surface-strong text-text shadow-sm"
                            : "text-text-muted hover:text-text",
                    )}
                >
                    Sign Up
                </button>
            </div>
        </div>
    );
}

export default function AuthBase({ onSubmit }: AuthProps) {
    const auth = getAuth();
    const { mode, setMode } = useAuth();

    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [username, setUserName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const isSignup = mode === "signup";
    const isLogin = mode === "login";
    const isReset = mode === "passwordReset";

    const handlePasswordReset = async () => {
        try {
            await sendPasswordResetEmail(auth, email);
            toast.success(`Password reset sent to ${email} (check spam).`);
        } catch {
            toast.error("Could not reset password.");
        }
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (isReset) {
            await handlePasswordReset();
            return;
        }

        await onSubmit(email, password, username, firstName, lastName);
    };

    return (
        <section className="w-full max-w-xl rounded-xl border border-border bg-surface p-6 shadow-soft backdrop-blur-md sm:p-7">
            <AuthHeader mode={mode} />
            {(isLogin || isSignup) && <ModePills mode={mode} setMode={setMode} />}

            <form onSubmit={handleSubmit} className="flex w-full flex-col gap-4">
                {isSignup && (
                    <>
                        <InputTextForm
                            variant="auth"
                            value={username}
                            id="username"
                            type="text"
                            name="username"
                            label="Username"
                            placeholder="freddy"
                            onChange={(e) => setUserName(e.target.value)}
                        />
                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                            <InputTextForm
                                variant="auth"
                                value={firstName}
                                id="first-name"
                                type="text"
                                name="firstName"
                                label="First Name"
                                placeholder="Freddy"
                                onChange={(e) => setFirstName(e.target.value)}
                            />
                            <InputTextForm
                                variant="auth"
                                value={lastName}
                                id="last-name"
                                type="text"
                                name="lastName"
                                label="Last Name"
                                placeholder="Body"
                                onChange={(e) => setLastName(e.target.value)}
                            />
                        </div>
                    </>
                )}

                <InputTextForm
                    variant="auth"
                    value={email}
                    id="email"
                    type="email"
                    name="email"
                    label="Email"
                    placeholder="you@example.com"
                    onChange={(e) => setEmail(e.target.value)}
                />

                {!isReset && (
                    <div>
                        <InputTextForm
                            variant="auth"
                            value={password}
                            id="password"
                            type="password"
                            name="password"
                            label="Password"
                            placeholder="••••••••"
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        {isLogin && (
                            <button
                                type="button"
                                onClick={() => setMode("passwordReset")}
                                className="mt-2 text-sm font-medium text-accent hover:text-accent-strong"
                            >
                                Forgot Password?
                            </button>
                        )}
                    </div>
                )}

                <div className="mt-2 flex flex-col gap-2">
                    <Button
                        type="submit"
                        color="authPrimary"
                        size="md"
                        className="w-full rounded-lg"
                    >
                        {isLogin ? "Log In" : isSignup ? "Sign Up" : "Send Password Reset"}
                    </Button>

                    {isReset && (
                        <Button
                            type="button"
                            color="authGhost"
                            size="md"
                            className="w-full rounded-lg"
                            onClick={() => setMode("login")}
                        >
                            Back to Login
                        </Button>
                    )}
                </div>
            </form>
        </section>
    );
}
