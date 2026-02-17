import api from "../config/api";

export interface UserBase {
  first_name: string;
  last_name: string;
  email: string;
}
interface UserCreate extends UserBase {
  password: string;
}

interface UserDB extends UserBase {
  id: string;
}
export default class UserManager {
  private static readonly base = "/users";

  static async signUp(data: UserCreate): Promise<UserDB> {
    try {
      const response = await api.post(this.base, data);
      return response.data;
    } catch (error: any) {
      const message =
        error.response?.data?.detail ||
        "Something went wrong. Please try again.";

      throw new Error(message);
    }
  }
}
