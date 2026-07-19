"use server";

import { submitAttendance } from "@/lib/api/academy/delivery";
import type { SubmitAttendanceCommand } from "./types";
import { errorMessage } from "@/shared/types/api";
import { revalidatePath } from "next/cache";

export async function submitAttendanceAction(sessionId: string, cmd: SubmitAttendanceCommand) {
  const result = await submitAttendance(sessionId, cmd);
  if (result.error) {
    return { error: errorMessage(result.error) };
  }
  revalidatePath("/");
  revalidatePath(`/sessions/${sessionId}`);
  return { success: true };
}
