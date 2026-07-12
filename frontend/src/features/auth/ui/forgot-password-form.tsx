"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { authApi } from "@/features/auth/api";
import { forgotPasswordSchema, type ForgotPasswordFormData } from "@/features/auth/schemas";
import { Button } from "@/shared/ui/button";
import { Input } from "@/shared/ui/input";
import { Label } from "@/shared/ui/label";
import { Alert } from "@/shared/ui/alert";
import { LoadingSpinner } from "@/shared/ui/loading-spinner";

export function ForgotPasswordForm() {
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
  });

  async function onSubmit(data: ForgotPasswordFormData) {
    setError(null);
    const result = await authApi.forgotPassword(data.email);
    if (result.error) {
      setError(result.error.error?.message || result.error.detail || "Failed to send email");
    } else {
      setSubmitted(true);
    }
  }

  if (submitted) {
    return (
      <div className="text-center space-y-4">
        <Alert>Check your email for a password reset link.</Alert>
        <Link href="/login" className="text-primary hover:underline">
          Back to login
        </Link>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && <Alert variant="destructive">{error}</Alert>}
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" {...register("email")} />
        {errors.email && <p className="text-sm text-destructive">{errors.email.message}</p>}
      </div>
      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? <LoadingSpinner className="h-4 w-4" /> : "Send reset link"}
      </Button>
      <p className="text-sm text-center">
        <Link href="/login" className="text-primary hover:underline">
          Back to login
        </Link>
      </p>
    </form>
  );
}
