import { apiAuth } from "@/shared/lib/api-client";
import type { ApiResult } from "@/shared/types/api";
import type { StudentProfileView, StudentEnrollmentView } from "@/features/student-operations/types";
import { cookies } from "next/headers";

async function getToken() {
  const cookieStore = await cookies();
  return cookieStore.get("auth_token")?.value || "";
}

export async function getStudentProfile(studentId: string): Promise<ApiResult<StudentProfileView>> {
  const token = await getToken();
  return apiAuth<StudentProfileView>(`/api/v1/academy/students/${studentId}`, token, {
    next: { tags: [`academy-students-${studentId}`] }
  });
}

export async function getStudentEnrollments(studentId: string): Promise<ApiResult<StudentEnrollmentView[]>> {
  const token = await getToken();
  return apiAuth<StudentEnrollmentView[]>(`/api/v1/academy/students/${studentId}/enrollments`, token, {
    next: { tags: [`academy-student-enrollments-${studentId}`] }
  });
}
