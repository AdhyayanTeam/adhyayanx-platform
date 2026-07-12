"use client";

import { useAuth } from "@/features/auth";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import { Separator } from "@/shared/ui/separator";

export default function ProfilePage() {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Profile</h1>

      <Card>
        <CardHeader>
          <CardTitle>Personal Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="text-sm text-muted-foreground">Name</p>
            <p className="font-medium">{user?.name}</p>
          </div>
          <Separator />
          <div>
            <p className="text-sm text-muted-foreground">Email</p>
            <p className="font-medium">{user?.email}</p>
          </div>
          <Separator />
          <div>
            <p className="text-sm text-muted-foreground">Email Verified</p>
            <p className="font-medium">{user?.is_verified ? "Yes" : "No"}</p>
          </div>
          <Separator />
          <div>
            <p className="text-sm text-muted-foreground">Status</p>
            <p className="font-medium capitalize">{user?.lifecycle_state}</p>
          </div>
          <Separator />
          <div>
            <p className="text-sm text-muted-foreground">Auth Provider</p>
            <p className="font-medium capitalize">{user?.auth_provider}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
