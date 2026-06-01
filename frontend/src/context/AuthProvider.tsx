import { createContext, useContext, useState, useEffect } from "react";
import {
    onAuthStateChanged,
    signInWithEmailAndPassword,
    signOut,
    getIdToken,
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

}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [userData, setUserData] = useState<UserRead | null>(null)
    const [loading, setLoading] = useState(true);
    const [mode, setMode] = useState<AuthMode>("login");

    useEffect(() => {
        const unSubscribe = onAuthStateChanged(auth, async (fbUser) => {
            if (!fbUser) {
                console.log("No User Logged In");
                setUser(null);
                setUserData(null);
                setLoading(false);
                return;
            }

            try {
                const token = await getIdToken(fbUser);
                console.log(token)
                const data = await UserManager.getCurrentUser(token);
                setUser(fbUser);
                setUserData(data);
          
            } catch (error) {
                console.error("Error fetching user data:", error);
                setUser(null);
                setUserData(null);
            } finally {
                setLoading(false);
            }
        });

        return () => unSubscribe();
    }, []);

    async function login(email: string, password: string) {
        return await signInWithEmailAndPassword(auth, email, password);
    }

    async function logout() {
        await signOut(auth);
        window.location.reload();
    }


    return (
        <AuthContext.Provider value={{ user, userData, loading, login, logout,  mode, setMode }}>
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
