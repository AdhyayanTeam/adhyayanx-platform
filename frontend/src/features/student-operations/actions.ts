"use server";

import { revalidatePath } from "next/cache";
import { assignBatch } from "@/lib/api/academy/enrollments";
import { errorMessage } from "@/shared/lib/api-client";

export async function submitBatchAssignment(studentId: string, enrollmentId: string, batchId: string) {
  const result = await assignBatch(enrollmentId, { batch_id: batchId });
  if (result.error) {
    return { success: false as const, error: errorMessage(result.error) };
  }
  
  revalidatePath(`/console/academy/students/${studentId}`);
  return { success: true as const };
}
