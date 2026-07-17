"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import type { CreateCourseRequest } from "../types";

interface CreateCourseFormProps {
  onSubmit: (data: CreateCourseRequest) => Promise<void>;
  onCancel: () => void;
}

export function CreateCourseForm({ onSubmit, onCancel }: CreateCourseFormProps) {
  const { register, handleSubmit, formState: { errors } } = useForm<CreateCourseRequest>();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFormSubmit = async (data: CreateCourseRequest) => {
    setIsSubmitting(true);
    try {
      await onSubmit(data);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="flex flex-col gap-4 bg-white p-6 rounded-lg border border-gray-200">
      <h3 className="text-lg font-semibold">Create New Course</h3>
      
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium" htmlFor="title">Course Title</label>
        <input
          id="title"
          className="border rounded px-3 py-2"
          {...register("title", { required: "Title is required" })}
        />
        {errors.title && <span className="text-sm text-red-500">{errors.title.message}</span>}
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium" htmlFor="description">Description (Optional)</label>
        <textarea
          id="description"
          className="border rounded px-3 py-2"
          rows={3}
          {...register("description")}
        />
      </div>

      <div className="flex justify-end gap-2 mt-4">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSubmitting}
          className="px-4 py-2 border rounded hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {isSubmitting ? "Creating..." : "Create Course"}
        </button>
      </div>
    </form>
  );
}
