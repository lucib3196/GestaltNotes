export type ValidRole = "educator" | "student" | "admin";

export interface UserBase {
  first_name: string;
  last_name: string;
  username: string | null;
}

export interface UserCreate extends UserBase {
  password: string;
  email: string;
  role?: ValidRole;
  course_id?: string | null;
}

export interface UserRead extends UserBase {
  email: string | null;
  force_password_reset: boolean;
  roles: ValidRole[]
}

export interface UserResponse extends UserBase {
  id: string;
  email: string;
}

export interface DeleteUserResponse {
  detail: string;
}
