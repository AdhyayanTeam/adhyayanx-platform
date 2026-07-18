"use client";

import { useEffect, useState, useCallback } from "react";
import { useAuth } from "@/features/auth/auth-context";
import { catalogApi } from "@/features/academy/catalog/api";
import { CreateCourseForm } from "@/features/academy/catalog/components/CreateCourseForm";
import type { Course, CreateCourseRequest } from "@/features/academy/catalog/types";

export default function CatalogPage() {
  const { silentRefresh, user } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const fetchCourses = useCallback(async () => {
    try {
      const token = await silentRefresh();
      if (!token) return;
      const result = await catalogApi.listCourses(token);
      if (result.data) {
        setCourses(result.data);
      }
    } catch (error) {
      console.error("Failed to load courses", error);
    } finally {
      setIsLoading(false);
    }
  }, [silentRefresh]);

  useEffect(() => {
    if (user) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      fetchCourses();
    }
  }, [user, fetchCourses]);

  const handleCreateCourse = async (data: CreateCourseRequest) => {
    const token = await silentRefresh();
    if (!token) return;
    const result = await catalogApi.createCourse(token, data);
    if (result.data) {
      setShowCreateForm(false);
      fetchCourses();
    } else {
      alert("Failed to create course. Ensure you have proper permissions.");
    }
  };

  const handlePublish = async (courseId: string) => {
    const token = await silentRefresh();
    if (!token) return;
    const result = await catalogApi.publishCourse(token, courseId);
    if (result.data) {
      fetchCourses();
    } else {
      alert("Failed to publish course. Ensure you have proper permissions.");
    }
  };

  const handleArchive = async (courseId: string) => {
    const token = await silentRefresh();
    if (!token) return;
    const result = await catalogApi.archiveCourse(token, courseId);
    if (result.data) {
      fetchCourses();
    } else {
      alert("Failed to archive course. Ensure you have proper permissions.");
    }
  };

  if (isLoading) {
    return <div className="p-8">Loading catalog...</div>;
  }

  return (
    <div className="p-8 max-w-5xl mx-auto flex flex-col gap-8">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Academic Catalog</h1>
        <button
          onClick={() => setShowCreateForm(true)}
          className="px-4 py-2 bg-black text-white rounded hover:bg-gray-800"
        >
          New Course
        </button>
      </div>

      {showCreateForm && (
        <CreateCourseForm 
          onSubmit={handleCreateCourse} 
          onCancel={() => setShowCreateForm(false)} 
        />
      )}

      <div className="flex flex-col gap-4">
        {courses.length === 0 ? (
          <div className="p-8 border border-dashed rounded text-center text-gray-500">
            No courses in the catalog yet.
          </div>
        ) : (
          courses.map((course) => (
            <div key={course.id} className="p-4 border rounded bg-white flex justify-between items-center shadow-sm">
              <div className="flex flex-col">
                <span className="font-semibold text-lg">{course.title}</span>
                <span className="text-gray-500 text-sm">{course.description || "No description"}</span>
              </div>
              
              <div className="flex items-center gap-4">
                <span className={`px-2 py-1 rounded text-xs font-medium border
                  ${course.lifecycle_state === "draft" ? "bg-yellow-100 text-yellow-800 border-yellow-200" : ""}
                  ${course.lifecycle_state === "published" ? "bg-green-100 text-green-800 border-green-200" : ""}
                  ${course.lifecycle_state === "archived" ? "bg-gray-100 text-gray-800 border-gray-200" : ""}
                `}>
                  {course.lifecycle_state.toUpperCase()}
                </span>
                
                <div className="flex gap-2">
                  {course.lifecycle_state === "draft" && (
                    <button 
                      onClick={() => handlePublish(course.id)}
                      className="text-sm px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                    >
                      Publish
                    </button>
                  )}
                  {course.lifecycle_state !== "archived" && (
                    <button 
                      onClick={() => handleArchive(course.id)}
                      className="text-sm px-3 py-1 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
                    >
                      Archive
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
