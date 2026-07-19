export interface SessionAttendanceSheetView {
  student_id: string;
  name: string;
  email: string;
  status: "PRESENT" | "ABSENT" | null;
}

export interface AttendanceSubmissionRecord {
  student_id: string;
  status: "PRESENT" | "ABSENT";
}

export interface SubmitAttendanceCommand {
  records: AttendanceSubmissionRecord[];
}
