import type { ApiResult } from "@/shared/types/api";

export async function api<T>(
  path: string,
  init?: RequestInit,
): Promise<ApiResult<T>> {
  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  try {
    const res = await fetch(`${base}${path}`, {
      credentials: "include",
      ...init,
      headers: { "Content-Type": "application/json", ...init?.headers },
    });
    if (res.status === 204) return { data: null as T, error: null };
    const body = await res.json();
    if (!res.ok) return { data: null, error: body };
    return { data: body as T, error: null };
  } catch (e) {
    return { data: null, error: { error: { code: "NETWORK", message: String(e) } } };
  }
}

export async function apiAuth<T>(
  path: string,
  token: string,
  init?: RequestInit,
): Promise<ApiResult<T>> {
  return api<T>(path, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      ...init?.headers,
    },
  });
}

export async function apiAuthRetry<T>(
  path: string,
  token: string,
  retryCallback: () => Promise<string | null>,
  init?: RequestInit,
): Promise<ApiResult<T>> {
  let result = await apiAuth<T>(path, token, init);
  if (result.error?.error?.code === "UNAUTHORIZED") {
    const newToken = await retryCallback();
    if (newToken) result = await apiAuth<T>(path, newToken, init);
  }
  return result;
}
