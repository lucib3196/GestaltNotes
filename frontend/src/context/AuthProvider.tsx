import { createContext, useContext, useState, useEffect } from "react";
import {
    onAuthStateChanged,
    signInWithEmailAndPassword,
    signOut,
    type User,
} from "firebase/auth";
import { auth } from "../firebase/initialization";

interface AuthContextType {
    user: User | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    getIdToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() =>
        onAuthStateChanged(auth, (fbuser) => {
            if (fbuser) {
                setUser(fbuser);
                setLoading(false);
                // User is signed in, see docs for a list of available properties
                // https://firebase.google.com/docs/reference/js/auth.user
                const uid = fbuser.uid;
                return uid;
                // ...
            } else {
                console.log("No User Signed in");
            }
        }),
    );

    async function login(email: string, password: string) {
        await signInWithEmailAndPassword(auth, email, password);
    }
    async function logout() {
        await signOut(auth);
        window.location.reload()
    }
    async function getIdToken() {
        if (!user) return null;
        return await user.getIdToken();
    }

    return (
        <AuthContext.Provider value={{ user, loading, login, logout, getIdToken }}>
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
