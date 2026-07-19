import { apiAuth } from "@/shared/lib/api-client";
import type { ApiResult } from "@/shared/types/api";
import type { 
  EnquiryPipelineItemView, 
  EnquiryDetailsView, 
  RecordFollowUpCommand, 
  MarkEnquiryLostCommand 
} from "@/features/admissions/types";
import { cookies } from "next/headers";

async function getToken() {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;
  return token || "";
}

export async function getPipeline(status?: string): Promise<ApiResult<EnquiryPipelineItemView[]>> {
  const token = await getToken();
  let url = "/api/v1/academy/admissions/pipeline";
  if (status) {
    url += `?status=${status}`;
  }
  return apiAuth<EnquiryPipelineItemView[]>(url, token, {
    next: { tags: ["academy-admissions-pipeline"] }
  });
}

export async function getEnquiryDetails(enquiryId: string): Promise<ApiResult<EnquiryDetailsView>> {
  const token = await getToken();
  return apiAuth<EnquiryDetailsView>(`/api/v1/academy/admissions/enquiries/${enquiryId}`, token, {
    next: { tags: [`academy-admissions-enquiries-${enquiryId}`] }
  });
}

export async function recordFollowUp(enquiryId: string, cmd: RecordFollowUpCommand): Promise<ApiResult<void>> {
  const token = await getToken();
  return apiAuth<void>(`/api/v1/academy/admissions/enquiries/${enquiryId}/follow-up`, token, {
    method: "POST",
    body: JSON.stringify(cmd)
  });
}

export async function admitEnquiry(enquiryId: string): Promise<ApiResult<void>> {
  const token = await getToken();
  return apiAuth<void>(`/api/v1/academy/admissions/enquiries/${enquiryId}/admit`, token, {
    method: "POST",
  });
}

export async function markEnquiryLost(enquiryId: string, cmd: MarkEnquiryLostCommand): Promise<ApiResult<void>> {
  const token = await getToken();
  return apiAuth<void>(`/api/v1/academy/admissions/enquiries/${enquiryId}/mark-lost`, token, {
    method: "POST",
    body: JSON.stringify(cmd)
  });
}
