"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { User, Organization } from "./types";
import { authApi } from "./api";

type AuthContextType = {
  user: User | null;
  organization: Organization | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<string | null>;
  logout: () => Promise<void>;
  silentRefresh: () => Promise<string | null>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const silentRefresh = useCallback(async (): Promise<string | null> => {
    const result = await authApi.refresh();
    if (result.data) {
      document.cookie = `auth_token=${result.data.access_token}; path=/; max-age=86400`;
      return result.data.access_token;
    }
    return null;
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function loadUser() {
      try {
        const refreshResult = await authApi.refresh();
        if (cancelled) return;
        if (!refreshResult.data) {
          setIsLoading(false);
          return;
        }
        const token = refreshResult.data.access_token;
        document.cookie = `auth_token=${token}; path=/; max-age=86400`;
        const meResult = await authApi.me(token);
        if (cancelled) return;
        if (meResult.data) {
          setUser(meResult.data.user);
          setOrganization(meResult.data.organization);
        }
      } catch {
        // ignore
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    loadUser();
    return () => { cancelled = true; };
  }, []);

  const login = useCallback(async (email: string, password: string): Promise<string | null> => {
    const result = await authApi.login(email, password);
    if (result.error) return result.error.error?.message || result.error.detail || "Login failed";
    document.cookie = `auth_token=${result.data!.access_token}; path=/; max-age=86400`;
    setUser(result.data!.user);
    setOrganization(result.data!.organization);
    return null;
  }, []);

  const logout = useCallback(async () => {
    const token = user?.id ? "" : "";
    await authApi.logout(token);
    document.cookie = "auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    setUser(null);
    setOrganization(null);
    router.push("/login");
  }, [router, user]);

  return (
    <AuthContext.Provider value={{ user, organization, isLoading, login, logout, silentRefresh }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
