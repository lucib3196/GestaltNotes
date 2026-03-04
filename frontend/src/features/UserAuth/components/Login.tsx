import AuthBase from "./AuthBase";
import { useAuth } from "../../../context";
import { UserManager } from "../../../services";
import { toast } from "react-toastify";
import { useEffect, useState } from "react";
import { type UserRead } from "../../../services/userManager";
export default function LogInForm() {
  const { login, setMode } = useAuth();
  const handleSubmit = async (email: string, password: string) => {
    try {
      login(email, password);
      toast.success("Log In Successful");
    } catch (error: any) {
      toast.error(`Could not Log In ${error as string}`);
    } finally {
      setMode("login-success");
    }
  };
  return <AuthBase onSubmit={handleSubmit} />;
}

export function LoginSuccess() {
  const { user } = useAuth();
  const [userData, setUserData] = useState<UserRead | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!user) return;

      try {
        const token = await user.getIdToken();
        const data = await UserManager.getUserInfo(token);
        setUserData(data);
      } catch (error) {
        console.error("Failed to fetch user info:", error);
      }
    };

    fetchData();
  }, [user]);

  return (
    <div className=" flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md bg-white p-8 text-center flex flex-col gap-4">
        <div className="text-2xl font-semibold text-gray-800">
          🎉 Login Successful
        </div>

        <p className="text-gray-500">Welcome back</p>

        <div className="bg-gray-100 rounded-lg p-4 text-sm text-gray-700">
          {userData ? (
            <div className="flex flex-col gap-1">
              <span className="font-medium">Email</span>
              <span>{userData.email}</span>
            </div>
          ) : (
            <span>Loading user info...</span>
          )}
        </div>
      </div>
    </div>
  );
}
