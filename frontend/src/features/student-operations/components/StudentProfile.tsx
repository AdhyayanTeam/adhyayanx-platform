import Link from "next/link";
import { format } from "date-fns";
import { AssignBatchDialog } from "./AssignBatchDialog";
import { Button } from "@/shared/ui/button";
import { ArrowLeft, BookOpen, Clock, User, Phone, Mail, GraduationCap } from "lucide-react";
import type { StudentProfileView, StudentEnrollmentView, CompatibleBatchView } from "../types";

interface EnrollmentWithBatches {
  enrollment: StudentEnrollmentView;
  compatibleBatches: CompatibleBatchView[];
}

interface Props {
  studentId: string;
  student: StudentProfileView;
  enrollmentsWithBatches: EnrollmentWithBatches[];
}

export function StudentProfile({ studentId, student, enrollmentsWithBatches }: Props) {
  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <Button variant="ghost" size="sm" className="mb-4 text-gray-500 hover:text-gray-900" render={<Link href="/academy/admissions" />}>
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to Admissions
        </Button>
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{student.name}</h1>
            <div className="mt-2 flex items-center space-x-6 text-sm text-gray-500">
              <span className="flex items-center">
                <Phone className="w-4 h-4 mr-2" />
                {student.phone}
              </span>
              {student.email && (
                <span className="flex items-center">
                  <Mail className="w-4 h-4 mr-2" />
                  {student.email}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Enrollments */}
        <div className="lg:col-span-2 space-y-6">
          <h2 className="text-lg font-semibold text-gray-900 border-b pb-2">Active Enrollments</h2>

          {enrollmentsWithBatches.length === 0 ? (
            <p className="text-gray-500 italic">This student has no active enrollments.</p>
          ) : (
            <div className="space-y-4">
              {enrollmentsWithBatches.map(({ enrollment, compatibleBatches }) => (
                <div key={enrollment.enrollment_id} className="bg-white border rounded-xl p-6 shadow-sm">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {enrollment.status.toUpperCase()}
                        </span>
                        <span className="text-xs text-gray-500 flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          Enrolled {format(new Date(enrollment.enrolled_at), "MMM d, yyyy")}
                        </span>
                      </div>
                      <h3 className="text-xl font-bold text-gray-900 flex items-center">
                        <BookOpen className="w-5 h-5 mr-2 text-indigo-500" />
                        {enrollment.course_title}
                      </h3>
                    </div>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-500 mb-1">Current Batch</p>
                      {enrollment.current_batch_id ? (
                        <div className="flex items-center">
                          <GraduationCap className="w-4 h-4 mr-2 text-gray-700" />
                          <span className="font-semibold text-gray-900">{enrollment.current_batch_name}</span>
                        </div>
                      ) : (
                        <span className="text-amber-600 font-medium flex items-center">
                          <span className="w-2 h-2 rounded-full bg-amber-500 mr-2"></span>
                          Unassigned
                        </span>
                      )}
                    </div>

                    <div>
                      <AssignBatchDialog
                        studentId={studentId}
                        enrollmentId={enrollment.enrollment_id}
                        courseTitle={enrollment.course_title}
                        currentBatchId={enrollment.current_batch_id}
                        compatibleBatches={compatibleBatches}
                        trigger={
                          <Button variant={enrollment.current_batch_id ? "outline" : "default"} size="sm">
                            {enrollment.current_batch_id ? "Change Batch" : "Assign Batch"}
                          </Button>
                        }
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Column: Profile details */}
        <div>
          <div className="bg-white border rounded-xl p-6 shadow-sm sticky top-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 border-b pb-2">Student Details</h2>
            <dl className="space-y-4">
              <div>
                <dt className="text-sm font-medium text-gray-500">Student ID</dt>
                <dd className="mt-1 text-sm text-gray-900 font-mono break-all">{student.id}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Primary Contact</dt>
                <dd className="mt-1 text-sm text-gray-900">{student.phone}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
}
