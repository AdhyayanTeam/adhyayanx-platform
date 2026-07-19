import { apiAuth, getToken } from "../fetcher";
import type { ApiResult } from "@/shared/types/api";

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
