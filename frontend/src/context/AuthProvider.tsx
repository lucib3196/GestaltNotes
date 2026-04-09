import { createContext, useContext, useState, useEffect } from "react";
import {
    onAuthStateChanged,
    signInWithEmailAndPassword,
    signOut,
    type User,
    type UserCredential,
} from "firebase/auth";
import { auth } from "../config/firebase_init";
import UserManager from "../services/userManager";

export type AuthMode = "login" | "signup" | "authenticate" | "passwordReset" | "login-success"

interface AuthContextType {
    user: User | null;
    role: string | null;
    loading: boolean;
    mode: AuthMode;
    setMode: (val: AuthMode) => void;
    login: (email: string, password: string) => Promise<UserCredential>;
    logout: () => void;
    getIdToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [role, setRole] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [mode, setMode] = useState<AuthMode>("login");

    useEffect(() =>
        onAuthStateChanged(auth, async (fbuser) => {
            if (fbuser) {
                setUser(fbuser);
                try {
                    const token = await fbuser.getIdToken();
                    const me = await UserManager.getMe(token);
                    const userRole = me.roles?.[0] ?? null;
                    setRole(userRole);
                } catch (e) {
                    console.error("Failed to fetch user role", e);
                    setRole(null);
                }
                setLoading(false);
            } else {
                setUser(null);
                setRole(null);
                setLoading(false);
            }
        })
    );

    async function login(email: string, password: string) {
        return await signInWithEmailAndPassword(auth, email, password);
    }

    async function logout() {
        await signOut(auth);
        setRole(null);
        window.location.reload();
    }

    async function getIdToken() {
        if (!user) return null;
        return await user.getIdToken();
    }

    return (
        <AuthContext.Provider value={{ user, role, loading, login, logout, getIdToken, mode, setMode }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}