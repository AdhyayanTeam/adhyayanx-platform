import { apiAuth } from "@/shared/lib/api-client";
import type { ApiResult } from "@/shared/types/api";
import { cookies } from "next/headers";

async function getToken() {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;
  return token || "";
}

export interface AssignBatchCommand {
  batch_id: string;
}

export async function assignBatch(enrollmentId: string, cmd: AssignBatchCommand): Promise<ApiResult<{ id: string }>> {
  const token = await getToken();
  return apiAuth<{ id: string }>(`/api/v1/academy/enrollments/${enrollmentId}/assign`, token, {
    method: "POST",
    body: JSON.stringify(cmd),
  });
}
