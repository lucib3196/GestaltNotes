import { useEffect } from "react";
import { useAuth } from "../../../../context";
import LogInForm from "./Login";
import { SignUpForm } from "./SignUp";
import PasswordResetForm from "./PasswordResetForm";
import { Navigate } from "react-router-dom";

export default function AuthPage() {
    const { mode, user, userData, setMode } = useAuth();

    useEffect(() => {
        if (userData?.force_password_reset) {
            setMode("passwordReset");
        }
    }, [userData?.force_password_reset, setMode]);


    if (user && mode !== "passwordReset") {
        return <Navigate to="/" replace />;
    }

    return (
        <div className="mx-auto flex w-full max-w-7xl items-center justify-center px-4 py-10 sm:px-6 lg:px-8">
            {mode === "login" && <LogInForm />}
            {mode === "signup" && <SignUpForm />}
            {mode === "passwordReset" && <PasswordResetForm />}
        </div>
    );
}
