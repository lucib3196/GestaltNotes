import { useAuth } from "../../../context";
import * as React from "react";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import type { AuthMode } from "../../../context";
import LogInForm from "./Login";
import { SignUpForm } from "./SignUp";

export default function AuthPage() {
    const { mode, setMode } = useAuth();

    const handleModeSwitch = (
        event: React.MouseEvent<HTMLElement>,
        newMode: AuthMode | string | null
    ) => {
        console.log(event, newMode)
        if (!newMode) return;

        setMode(newMode as AuthMode);
    };

    return (
        <div className="flex flex-col justify-center items-center">
            <ToggleButtonGroup
                value={mode}
                exclusive
                onChange={handleModeSwitch}
                aria-label="text alignment"
            >
                <ToggleButton value="signup" aria-label="left aligned">
                    SignUp
                </ToggleButton>

                <ToggleButton value="login" aria-label="justified" >
                    Log In
                </ToggleButton>
            </ToggleButtonGroup>
            {mode === "login" ? <LogInForm /> : mode === "signup" ? <SignUpForm /> : ""}
        </div>
    );
}
