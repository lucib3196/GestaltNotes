import { useAuth } from "../../../context";
import { Section } from "../../../components/Section";
import { UserManager } from "../../../services";
import { Button } from "../../../components/Button";
export default function UserPage() {
    const { user } = useAuth();
    const fetchData = async () => {
        const token = await user?.getIdToken();
        const data = await UserManager.getUserInfo(token);
        console.log(data)
    };

    fetchData();

    return (
        <Section className="mx-auto flex min-h-screen w-full max-w-3xl p-4 md:p-6">
            <div className="flex w-full flex-col gap-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                <header className="border-b border-slate-200 pb-4 text-center">
                    <h1 className="text-2xl font-semibold text-slate-900">My Account</h1>
                </header>
                <div className="mx-auto flex w-full max-w-sm flex-col gap-3">
                    <h2 className="text-center text-lg font-medium text-slate-800">Account Settings</h2>
                    <Button>Edit Profile</Button>
                    <Button>Change Password</Button>
                    <Button>Logout</Button>
                </div>
            </div>
        </Section>
    );
}
