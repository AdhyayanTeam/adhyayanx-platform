import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import { VerifyEmailClient } from "@/features/auth/ui/verify-email-client";

export default function VerifyEmailPage({
  searchParams,
}: {
  searchParams: Promise<{ token?: string }>;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">Email Verification</CardTitle>
        </CardHeader>
        <CardContent className="flex justify-center">
          <VerifyEmailWrapper searchParams={searchParams} />
        </CardContent>
      </Card>
    </div>
  );
}

async function VerifyEmailWrapper({ searchParams }: { searchParams: Promise<{ token?: string }> }) {
  const params = await searchParams;
  const token = params.token;
  if (!token) return <p className="text-destructive">Invalid verification link</p>;
  return <VerifyEmailClient token={token} />;
}
