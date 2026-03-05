import { useAuth } from "../../../context";
import * as React from "react";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import type { AuthMode } from "../../../context";
import LogInForm, { LoginSuccess } from "./Login";
import { SignUpForm } from "./SignUp";

export default function AuthPage() {
    const { mode, setMode } = useAuth();

    const handleModeSwitch = (
        event: React.MouseEvent<HTMLElement>,
        newMode: AuthMode | string | null,
    ) => {
        console.log(event, newMode);
        if (!newMode) return;

        setMode(newMode as AuthMode);
    };

    return (
        <div className="flex items-center justify-center bg-gray-50">
            <div className="w-full  bg-white  p-8 flex flex-col gap-6">
                {/* Header */}
                <div className="text-center">
                    <h1 className="text-2xl font-semibold text-gray-800">Welcome</h1>
                    <p className="text-gray-500 text-sm mt-1">
                        Sign in or create an account
                    </p>
                </div>

                {/* Toggle */}
                {mode !== "login-success" && <div className="flex justify-center">
                    <ToggleButtonGroup value={mode} exclusive onChange={handleModeSwitch}>
                        <ToggleButton value="login">Log In</ToggleButton>
                        {/* <ToggleButton value="signup">Sign Up</ToggleButton> */}
                    </ToggleButtonGroup>
                </div>}

                {/* Form */}
                <div>
                    {mode === "login" && <LogInForm />}
                    {mode === "signup" && <SignUpForm />}
                    {mode === "login-success" && <LoginSuccess />}
                </div>
            </div>
        </div>
    );
}
