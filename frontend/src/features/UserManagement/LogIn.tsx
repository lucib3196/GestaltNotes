import AuthBase from "./AuthBase";
import { useAuth } from "../../context";
import { toast } from "react-toastify";

export default function LogInForm() {
    const { login } = useAuth();
    const handleSubmit = async (email: string, password: string) => {
        try {
            login(email, password);
            toast.success("Log In Successful");
        } catch (error: any) {
            toast.error(`Could not Log In ${error as string}`);
        }
    };
    return <AuthBase onSubmit={handleSubmit} />;
}
