export interface SessionAttendanceSheetView {
  student_id: string;
  name: string;
  email: string;
  status: "PRESENT" | "ABSENT" | null;
}

export interface SubmitAttendanceCommand {
  records: {
    student_id: string;
    status: "PRESENT" | "ABSENT";
  }[];
}
