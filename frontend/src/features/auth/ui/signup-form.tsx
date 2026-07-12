"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { authApi } from "@/features/auth/api";
import { signupSchema, type SignupFormData } from "@/features/auth/schemas";
import { Button } from "@/shared/ui/button";
import { Input } from "@/shared/ui/input";
import { Label } from "@/shared/ui/label";
import { Alert } from "@/shared/ui/alert";
import { LoadingSpinner } from "@/shared/ui/loading-spinner";

export function SignupForm() {
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
  });

  async function onSubmit(data: SignupFormData) {
    setError(null);
    const result = await authApi.signup({
      organization_name: data.organizationName,
      blueprint_code: "academy",
      owner_name: data.ownerName,
      email: data.email,
      password: data.password,
    });
    if (result.error) {
      setError(result.error.error?.message || result.error.detail || "Signup failed");
    } else {
      setSuccess(true);
    }
  }

  if (success) {
    return (
      <div className="text-center space-y-4">
        <Alert>Check your email for a verification link.</Alert>
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
        <Label htmlFor="organizationName">Organization Name</Label>
        <Input id="organizationName" {...register("organizationName")} />
        {errors.organizationName && <p className="text-sm text-destructive">{errors.organizationName.message}</p>}
      </div>
      <div className="space-y-2">
        <Label htmlFor="ownerName">Your Name</Label>
        <Input id="ownerName" {...register("ownerName")} />
        {errors.ownerName && <p className="text-sm text-destructive">{errors.ownerName.message}</p>}
      </div>
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" {...register("email")} />
        {errors.email && <p className="text-sm text-destructive">{errors.email.message}</p>}
      </div>
      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input id="password" type="password" {...register("password")} />
        {errors.password && <p className="text-sm text-destructive">{errors.password.message}</p>}
      </div>
      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? <LoadingSpinner className="h-4 w-4" /> : "Sign up"}
      </Button>
      <p className="text-sm text-center">
        Already have an account?{" "}
        <Link href="/login" className="text-primary hover:underline">
          Log in
        </Link>
      </p>
    </form>
  );
}
