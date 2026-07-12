export type ApiError = {
  error?: { code: string; message: string };
  detail?: string;
};

export type ApiResult<T> = { data: T; error: null } | { data: null; error: ApiError };

export function extractError(err: unknown): ApiError {
  if (err && typeof err === "object" && "error" in err) return err as ApiError;
  if (err && typeof err === "object" && "detail" in err) return err as ApiError;
  return { error: { code: "UNKNOWN", message: String(err) } };
}

export function errorMessage(err: ApiError): string {
  return err.error?.message || err.detail || "Something went wrong";
}
