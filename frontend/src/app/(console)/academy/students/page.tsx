import Link from "next/link";
import { listStudents } from "@/lib/api/academy/students";
import { errorMessage } from "@/shared/types/api";

export const metadata = {
  title: "Students",
};

export default async function StudentsListPage() {
  const result = await listStudents();

  if (result.error || !result.data) {
    return (
      <div className="p-8">
        <div className="bg-red-50 text-red-600 p-4 rounded-md">
          Failed to load students: {result.error ? errorMessage(result.error) : "No data"}
        </div>
      </div>
    );
  }

  const students = result.data;

  return (
    <div className="max-w-4xl p-6 lg:p-8">
      <header className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight text-neutral-900">Students</h1>
        <p className="text-neutral-500 mt-1">All students enrolled in your institute.</p>
      </header>

      {students.length === 0 ? (
        <div className="text-center py-20 bg-neutral-50 rounded-lg border border-neutral-200 border-dashed">
          <h3 className="text-lg font-medium text-neutral-900">No students yet</h3>
          <p className="text-neutral-500 mt-1">Students will appear here once they are admitted.</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-neutral-200 divide-y divide-neutral-200">
          {students.map((student) => (
            <Link
              key={student.id}
              href={`/academy/students/${student.id}`}
              className="flex items-center justify-between px-4 py-3 hover:bg-neutral-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-sm font-medium">
                  {student.name.charAt(0).toUpperCase()}
                </div>
                <div>
                  <p className="text-sm font-medium text-neutral-900">{student.name}</p>
                  <p className="text-xs text-neutral-500">{student.email}</p>
                </div>
              </div>
              <svg className="h-4 w-4 text-neutral-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
              </svg>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
