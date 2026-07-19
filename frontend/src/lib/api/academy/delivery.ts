import { apiAuth } from "@/shared/lib/api-client";
import type { ApiResult } from "@/shared/types/api";
import type { TodaySessionView } from "@/features/daily-operations/types";
import type { SessionAttendanceSheetView, SubmitAttendanceCommand } from "@/features/attendance/types";

// Helper to get token (server-side only for Server Actions/Components)
import { cookies } from "next/headers";

async function getToken() {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;
  return token || "";
}

export async function getTodaysSessions(date?: string): Promise<ApiResult<TodaySessionView[]>> {
  const token = await getToken();
  let url = "/api/v1/academy/delivery/sessions";
  if (date) {
    url += `?date=${date}`;
  }
  return apiAuth<TodaySessionView[]>(url, token, {
    next: { tags: ["academy", "delivery", "sessions"] }
  });
}

export async function getSessionAttendance(sessionId: string): Promise<ApiResult<SessionAttendanceSheetView[]>> {
  const token = await getToken();
  return apiAuth<SessionAttendanceSheetView[]>(`/api/v1/academy/delivery/sessions/${sessionId}/attendance`, token, {
    next: { tags: ["academy", "delivery", "attendance", sessionId] }
  });
}

export async function submitAttendance(sessionId: string, cmd: SubmitAttendanceCommand): Promise<ApiResult<void>> {
  const token = await getToken();
  return apiAuth<void>(`/api/v1/academy/delivery/sessions/${sessionId}/attendance`, token, {
    method: "POST",
    body: JSON.stringify(cmd)
  });
}

import type { BatchOverviewView, BatchRosterView, BatchSessionSummaryView } from "@/features/batch-operations/types";

export async function getBatchOverview(batchId: string): Promise<ApiResult<BatchOverviewView>> {
  const token = await getToken();
  return apiAuth<BatchOverviewView>(`/api/v1/academy/delivery/batches/${batchId}`, token, {
    next: { tags: ["academy", "delivery", "batches", batchId] }
  });
}

export async function getBatchRoster(batchId: string): Promise<ApiResult<BatchRosterView[]>> {
  const token = await getToken();
  return apiAuth<BatchRosterView[]>(`/api/v1/academy/delivery/batches/${batchId}/roster`, token, {
    next: { tags: ["academy", "delivery", "batches", batchId, "roster"] }
  });
}

export async function getBatchAttendanceSummary(batchId: string): Promise<ApiResult<BatchSessionSummaryView[]>> {
  const token = await getToken();
  return apiAuth<BatchSessionSummaryView[]>(`/api/v1/academy/delivery/batches/${batchId}/attendance-summary`, token, {
    next: { tags: ["academy", "delivery", "batches", batchId, "attendance"] }
  });
}
