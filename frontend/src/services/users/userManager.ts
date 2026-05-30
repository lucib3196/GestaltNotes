import api from "../../config/api";
import type { DeleteUserResponse, UserCreate, UserRead, UserResponse } from "./types";

export default class UserManager {
  private static readonly base = "/users";

  static async createUser(data: UserCreate): Promise<UserResponse> {
    const response = await api.post(`${this.base}/`, data);
    return response.data;
  }

  static async getCurrentUser(token: string): Promise<UserRead> {
    const response = await api.post(
      `${this.base}/get_current_user`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    return response.data;
  }

  static async getUserById(id: string, token: string): Promise<UserRead | null> {
    const response = await api.get(`${this.base}/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  }

  static async deleteUserById(id: string, token: string): Promise<DeleteUserResponse> {
    const response = await api.delete(`${this.base}/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  }

  static async resetTempPassword(newPassword: string, token: string): Promise<string> {
    const response = await api.post(
      `${this.base}/password_reset/temp`,
      { new_password: newPassword },
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    return response.data;
  }
}
