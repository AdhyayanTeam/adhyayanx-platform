"use server";

import { revalidatePath } from "next/cache";
import { recordFollowUp, admitEnquiry, markEnquiryLost } from "@/lib/api/academy/admissions";
import { errorMessage } from "@/shared/types/api";
import type { RecordFollowUpCommand, MarkEnquiryLostCommand } from "./types";

export async function submitFollowUp(enquiryId: string, cmd: RecordFollowUpCommand) {
  const result = await recordFollowUp(enquiryId, cmd);
  if (result.error) {
    return { success: false, error: errorMessage(result.error) };
  }
  
  revalidatePath("/console/academy/admissions");
  revalidatePath(`/console/academy/admissions/${enquiryId}`);
  return { success: true };
}

export async function submitAdmission(enquiryId: string) {
  const result = await admitEnquiry(enquiryId);
  if (result.error) {
    return { success: false, error: errorMessage(result.error) };
  }
  
  revalidatePath("/console/academy/admissions");
  revalidatePath(`/console/academy/admissions/${enquiryId}`);
  return { success: true };
}

export async function submitLost(enquiryId: string, cmd: MarkEnquiryLostCommand) {
  const result = await markEnquiryLost(enquiryId, cmd);
  if (result.error) {
    return { success: false, error: errorMessage(result.error) };
  }
  
  revalidatePath("/console/academy/admissions");
  revalidatePath(`/console/academy/admissions/${enquiryId}`);
  return { success: true };
}
