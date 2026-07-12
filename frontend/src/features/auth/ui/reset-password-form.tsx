"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { authApi } from "@/features/auth/api";
import { resetPasswordSchema, type ResetPasswordFormData } from "@/features/auth/schemas";
import { Button } from "@/shared/ui/button";
import { Input } from "@/shared/ui/input";
import { Label } from "@/shared/ui/label";
import { Alert } from "@/shared/ui/alert";
import { LoadingSpinner } from "@/shared/ui/loading-spinner";

export function ResetPasswordForm({ token }: { token: string }) {
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
  });

  async function onSubmit(data: ResetPasswordFormData) {
    setError(null);
    const result = await authApi.resetPassword(token, data.password);
    if (result.error) {
      setError(result.error.error?.message || result.error.detail || "Failed to reset password");
    } else {
      setSuccess(true);
    }
  }

  if (success) {
    return (
      <div className="text-center space-y-4">
        <Alert>Password reset successful.</Alert>
        <Link href="/login" className="text-primary hover:underline">
          Go to login
        </Link>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && <Alert variant="destructive">{error}</Alert>}
      <div className="space-y-2">
        <Label htmlFor="password">New Password</Label>
        <Input id="password" type="password" {...register("password")} />
        {errors.password && <p className="text-sm text-destructive">{errors.password.message}</p>}
      </div>
      <div className="space-y-2">
        <Label htmlFor="confirmPassword">Confirm Password</Label>
        <Input id="confirmPassword" type="password" {...register("confirmPassword")} />
        {errors.confirmPassword && <p className="text-sm text-destructive">{errors.confirmPassword.message}</p>}
      </div>
      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? <LoadingSpinner className="h-4 w-4" /> : "Reset password"}
      </Button>
    </form>
  );
}
