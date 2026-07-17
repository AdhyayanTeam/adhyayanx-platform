import { apiAuth } from "@/shared/lib/api-client";
import type { Course, CreateCourseRequest } from "./types";

export const catalogApi = {
  listCourses: (token: string) =>
    apiAuth<Course[]>("/api/v1/academy/catalog/courses", token),

  createCourse: (token: string, data: CreateCourseRequest) =>
    apiAuth<Course>("/api/v1/academy/catalog/courses", token, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  publishCourse: (token: string, courseId: string) =>
    apiAuth<Course>(`/api/v1/academy/catalog/courses/${courseId}/publish`, token, {
      method: "POST",
    }),

  archiveCourse: (token: string, courseId: string) =>
    apiAuth<Course>(`/api/v1/academy/catalog/courses/${courseId}/archive`, token, {
      method: "POST",
    }),
};
