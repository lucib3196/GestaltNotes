import { UserManager } from "../../services";
import AuthBase from "./AuthBase";
import { toast } from "react-toastify"

export function SignUpForm() {
    const onSubmit = async (
        email: string,
        password: string,
        firstName?: string,
        lastName?: string
    ) => {
        try {
            if (!firstName || !lastName) {
                toast.error("First name and last name are required");
                return;
            }

            await UserManager.signUp({
                first_name: firstName,
                last_name: lastName,
                email,
                password,
            });

            toast.success("Account created successfully!");
            
        } catch (error: any) {
            toast.error(error.message ?? "Failed to create account");
        }
    };

    return (
        <AuthBase onSubmit={onSubmit} />
    );
}
