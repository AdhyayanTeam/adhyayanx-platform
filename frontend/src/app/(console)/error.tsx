"use client";

import { Alert } from "@/shared/ui/alert";
import { Button } from "@/shared/ui/button";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="text-center space-y-4">
        <Alert variant="destructive">Something went wrong: {error.message}</Alert>
        <Button onClick={reset}>Try again</Button>
      </div>
    </div>
  );
}
