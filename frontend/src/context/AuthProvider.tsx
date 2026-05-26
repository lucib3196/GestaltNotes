import { createContext, useContext, useState, useEffect } from "react";
import {
    onAuthStateChanged,
    signInWithEmailAndPassword,
    signOut,
    type User,
    type UserCredential,
} from "firebase/auth";
import { auth } from "../config/firebase_init";
import { UserManager, type UserRead } from "../services";

export type AuthMode = "login" | "signup" | "authenticate" | "passwordReset" | "login-success"

interface AuthContextType {
    user: User | null;
    userData: UserRead | null
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
    const [userData, setUserData] = useState<UserRead | null>(null)
    const [loading, setLoading] = useState(true);
    const [mode, setMode] = useState<AuthMode>("login");

    useEffect(() =>
        onAuthStateChanged(auth, async (fbuser) => {
            if (fbuser) {
                setUser(fbuser);
                try {
                    const token = await fbuser.getIdToken();
                    const user = await UserManager.getCurrentUser(token);
                    setUserData(user)
                } catch (e) {
                    console.error("Failed to fetch user role", e);
                }
                setLoading(false);
            } else {
                setUser(null);
                setUserData(null)
                setLoading(false);
            }
        }),[user]
    );

    async function login(email: string, password: string) {
        return await signInWithEmailAndPassword(auth, email, password);
    }

    async function logout() {
        await signOut(auth);
        window.location.reload();
    }

    async function getIdToken() {
        if (!user) return null;
        return await user.getIdToken();
    }

    return (
        <AuthContext.Provider value={{ user, userData, loading, login, logout, getIdToken, mode, setMode }}>
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
