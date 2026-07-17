export interface Course {
  id: string;
  organization_id: string;
  title: string;
  description: string | null;
  lifecycle_state: "draft" | "published" | "archived";
}

export interface CreateCourseRequest {
  title: string;
  description?: string;
}
