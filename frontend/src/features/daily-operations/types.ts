export interface TodaySessionView {
  session_id: string;
  batch_id: string;
  course_title: string;
  batch_name: string;
  starts_at: string;
  ends_at: string;
  assigned_student_count: number;
  attendance_submitted_at: string | null;
}
