"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "@/features/auth";
import { ConsoleSidebar } from "@/features/auth/ui/console-sidebar";
import { LoadingSpinner } from "@/shared/ui/loading-spinner";

export default function ConsoleLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [isLoading, user, router]);

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="flex min-h-screen">
      <ConsoleSidebar />
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
