"use client";

import { useAuth } from "@/features/auth";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import { Separator } from "@/shared/ui/separator";

export default function OrganizationPage() {
  const { organization } = useAuth();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Organization</h1>

      <Card>
        <CardHeader>
          <CardTitle>Organization Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="text-sm text-muted-foreground">Name</p>
            <p className="font-medium">{organization?.name}</p>
          </div>
          <Separator />
          <div>
            <p className="text-sm text-muted-foreground">Slug</p>
            <p className="font-medium">{organization?.slug}</p>
          </div>
          <Separator />
          <div>
            <p className="text-sm text-muted-foreground">Status</p>
            <p className="font-medium capitalize">{organization?.lifecycle_state}</p>
          </div>
          <Separator />
          <div>
            <p className="text-sm text-muted-foreground">Created</p>
            <p className="font-medium">
              {organization?.created_at ? new Date(organization.created_at).toLocaleDateString() : "N/A"}
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
