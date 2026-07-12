"use client";

import { useAuth } from "@/features/auth";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";

export default function ConsoleHomePage() {
  const { user, organization } = useAuth();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Welcome, {user?.name}</h1>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">Profile</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-lg font-semibold">{user?.name}</p>
            <p className="text-sm text-muted-foreground">{user?.email}</p>
            <p className="text-sm text-muted-foreground mt-1">
              Status: {user?.lifecycle_state}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">Organization</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-lg font-semibold">{organization?.name}</p>
            <p className="text-sm text-muted-foreground">{organization?.slug}</p>
            <p className="text-sm text-muted-foreground mt-1">
              Status: {organization?.lifecycle_state}
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
