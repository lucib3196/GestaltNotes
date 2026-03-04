
import { UseAuthMode } from "./context";
import { InputTextForm } from "../../components/FormComponents";
import { useState } from "react";
import type { FormEvent } from "react";
interface AuthProps {
    onSubmit: (
        email: string,
        password: string,
        firstName?: string,
        lastName?: string,
    ) => Promise<void>;
}
import { Button } from "../../components/Button";

export default function AuthBase({ onSubmit }: AuthProps) {
    const { mode, setMode } = UseAuthMode();

    const [firstName, setFirstName] = useState<string>("");
    const [lastName, setLastName] = useState<string>("");

    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        await onSubmit(email, password, firstName, lastName)
        // onSubmit(email, password, firstName);
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="flex flex-col gap-y-5 items-center justify-center w-full h-full"
            id={""}
        >
            <div className="flex flex-col gap-y-2 gap-x-0 place-content-center justify-items-center w-fit mx-auto">
                {mode === "signup" && (
                    <>
                        <InputTextForm
                            value={firstName}
                            id="first-name"
                            type="text"
                            name="firstName"
                            label="First Name"
                            placeholder="Freddy"
                            onChange={(e) => setFirstName(e.target.value)}
                        />
                        <InputTextForm
                            value={lastName}
                            id="last-name"
                            type="text"
                            name="Last Name"
                            label="Last Name"
                            placeholder="Freddy"
                            onChange={(e) => setLastName(e.target.value)}
                        />
                    </>
                )}
                {/* Email field always show */}
                <InputTextForm
                    value={email}
                    id="email"
                    type="email"
                    name="email"
                    label="Email"
                    placeholder="FBody@email.com"
                    onChange={(e) => setEmail(e.target.value)}
                />

                {/* Password field — hidden only during password reset */}
                {mode !== "passwordReset" && (
                    <div>
                        <InputTextForm
                            value={password}
                            id="password"
                            type="password"
                            name="password"
                            label="Password"
                            placeholder="*********"
                            onChange={(e) => setPassword(e.target.value)}
                        />

                        {mode === "login" && (
                            <div
                                onClick={() => setMode("passwordReset")}
                                className="text-sm text-violet-300 cursor-pointer hover:underline mt-2"
                            >
                                Forgot Password?
                            </div>
                        )}
                    </div>

                )}
                {/* For layout purposes have the institution as the last element */}

            </div>

            <Button type="submit">
                {mode === "login"
                    ? "Log In"
                    : mode === "signup"
                        ? "Sign Up"
                        : mode === "passwordReset"
                            ? "Send Password Reset"
                            : "Continue"}
            </Button>
            {mode === "passwordReset" && (
                <Button
                    type="button" // prevent form submission
                    onClick={() => setMode("login")}
                    size="md"
                >
                    Go Back to Login
                </Button>
            )}
        </form>
    );
}
