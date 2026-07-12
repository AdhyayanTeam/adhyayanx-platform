import { api, apiAuth } from "@/shared/lib/api-client";
import type { LoginResponse, SignupResponse, MeResponse } from "./types";

export const authApi = {
  login: (email: string, password: string) =>
    api<LoginResponse>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  signup: (data: {
    organization_name: string;
    blueprint_code: string;
    owner_name: string;
    email: string;
    password: string;
  }) =>
    api<SignupResponse>("/api/v1/auth/signup", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  logout: (token: string) =>
    apiAuth<null>("/api/v1/auth/logout", token, { method: "POST" }),

  refresh: () =>
    api<{ access_token: string; token_type: string }>("/api/v1/auth/refresh", {
      method: "POST",
    }),

  me: (token: string) => apiAuth<MeResponse>("/api/v1/auth/me", token),

  forgotPassword: (email: string) =>
    api<{ message: string }>("/api/v1/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),

  resetPassword: (token: string, newPassword: string) =>
    api<{ message: string }>("/api/v1/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({ token, new_password: newPassword }),
    }),

  verifyEmail: (token: string) =>
    api<{ message: string }>("/api/v1/auth/verify-email", {
      method: "POST",
      body: JSON.stringify({ token }),
    }),
};
