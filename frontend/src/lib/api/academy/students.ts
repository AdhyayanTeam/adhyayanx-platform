import { apiAuth, getToken } from "../fetcher";
import type { ApiResult } from "@/shared/types/api";
import type { StudentProfileView, StudentEnrollmentView } from "@/features/student-operations/types";

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
