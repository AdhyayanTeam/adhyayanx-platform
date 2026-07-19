"use server";

import { revalidatePath } from "next/cache";
import { assignBatch } from "@/lib/api/academy/enrollments";
import { errorMessage } from "@/shared/types/api";

export async function submitBatchAssignment(studentId: string, enrollmentId: string, batchId: string) {
  const result = await assignBatch(enrollmentId, { batch_id: batchId });
  if (result.error) {
    return { success: false as const, error: errorMessage(result.error) };
  }
  
  revalidatePath(`/academy/students/${studentId}`);
  return { success: true as const };
}
