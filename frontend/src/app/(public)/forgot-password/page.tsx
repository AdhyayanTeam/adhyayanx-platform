import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import { ForgotPasswordForm } from "@/features/auth/ui/forgot-password-form";

export default function ForgotPasswordPage() {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">Forgot Password</CardTitle>
          <p className="text-sm text-muted-foreground">Enter your email to receive a reset link</p>
        </CardHeader>
        <CardContent>
          <ForgotPasswordForm />
        </CardContent>
      </Card>
    </div>
  );
}
