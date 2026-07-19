export interface StudentProfileView {
  id: string;
  organization_id: string;
  name: string;
  email: string;
  phone: string;
}

export interface StudentEnrollmentView {
  enrollment_id: string;
  course_id: string;
  course_title: string;
  status: string;
  enrolled_at: string;
  current_batch_id: string | null;
  current_batch_name: string | null;
}

export interface CompatibleBatchView {
  batch_id: string;
  course_title: string;
  batch_name: string;
  assigned_student_count: number;
  next_session_starts_at: string | null;
}
