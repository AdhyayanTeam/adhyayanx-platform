"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { authApi } from "@/features/auth/api";
import { Alert } from "@/shared/ui/alert";
import { LoadingSpinner } from "@/shared/ui/loading-spinner";

export function VerifyEmailClient({ token }: { token: string }) {
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("");

  useEffect(() => {
    let cancelled = false;
    async function verify() {
      const result = await authApi.verifyEmail(token);
      if (cancelled) return;
      if (result.error) {
        setStatus("error");
        setMessage(result.error.error?.message || result.error.detail || "Verification failed");
      } else {
        setStatus("success");
        setMessage(result.data?.message || "Email verified successfully");
      }
    }
    verify();
    return () => { cancelled = true; };
  }, [token]);

  if (status === "loading") return <LoadingSpinner />;

  return (
    <div className="text-center space-y-4">
      <Alert variant={status === "error" ? "destructive" : "default"}>{message}</Alert>
      <Link href="/login" className="text-primary hover:underline">
        Go to login
      </Link>
    </div>
  );
}
