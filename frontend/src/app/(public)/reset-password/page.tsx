import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import { ResetPasswordForm } from "@/features/auth/ui/reset-password-form";

export default function ResetPasswordPage({
  searchParams,
}: {
  searchParams: Promise<{ token?: string }>;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">Reset Password</CardTitle>
          <p className="text-sm text-muted-foreground">Enter your new password</p>
        </CardHeader>
        <CardContent>
          <ResetPasswordWrapper searchParams={searchParams} />
        </CardContent>
      </Card>
    </div>
  );
}

async function ResetPasswordWrapper({ searchParams }: { searchParams: Promise<{ token?: string }> }) {
  const params = await searchParams;
  const token = params.token;
  if (!token) return <p className="text-destructive text-center">Invalid reset link</p>;
  return <ResetPasswordForm token={token} />;
}
