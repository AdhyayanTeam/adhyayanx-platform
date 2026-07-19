export interface EnquiryPipelineItemView {
  enquiry_id: string;
  lead_id: string;
  lead_name: string;
  lead_phone: string;
  course_name: string;
  status: string;
  assigned_to: string | null;
  next_follow_up_at: string | null;
}

export interface EnquiryDetailsView {
  enquiry_id: string;
  lead_id: string;
  student_id: string | null;
  lead_name: string;
  lead_phone: string;
  lead_email: string | null;
  course_id: string;
  course_name: string;
  status: string;
  source: string;
  assigned_to: string | null;
  next_follow_up_at: string | null;
  notes: string | null;
  created_at: string;
}

export interface RecordFollowUpCommand {
  next_follow_up_at: string;
  notes: string;
}

export interface MarkEnquiryLostCommand {
  reason: string;
}
