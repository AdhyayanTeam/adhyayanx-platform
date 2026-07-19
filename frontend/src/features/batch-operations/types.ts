export interface BatchOverviewView {
  batch_id: string;
  course_title: string;
  batch_name: string;
  assigned_student_count: number;
  next_session_id: string | null;
  next_session_starts_at: string | null;
}

export interface BatchRosterView {
  student_id: string;
  name: string;
  email: string;
}

export interface BatchSessionSummaryView {
  session_id: string;
  starts_at: string;
  present_count: number;
  absent_count: number;
  attendance_submitted_at: string | null;
}
