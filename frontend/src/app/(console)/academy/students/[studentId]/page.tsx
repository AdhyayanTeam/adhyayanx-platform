import { notFound } from "next/navigation";
import { getStudentProfile, getStudentEnrollments } from "@/lib/api/academy/students";
import { getBatchesForCourse } from "@/lib/api/academy/delivery";
import { StudentProfile } from "@/features/student-operations/components/StudentProfile";

export default async function StudentProfilePage({ params }: { params: Promise<{ studentId: string }> }) {
  const { studentId } = await params;
  const [profileResult, enrollmentsResult] = await Promise.all([
    getStudentProfile(studentId),
    getStudentEnrollments(studentId),
  ]);

  if (profileResult.error || !profileResult.data) {
    if (profileResult.error?.status === 404) notFound();
    return (
      <div className="p-8 text-center text-red-600 bg-red-50 rounded-lg">
        Failed to load student profile.
      </div>
    );
  }

  const student = profileResult.data;
  const enrollments = enrollmentsResult.data || [];

  const enrollmentsWithBatches = await Promise.all(
    enrollments.map(async (enrollment) => {
      const batchesResult = await getBatchesForCourse(enrollment.course_id);
      return {
        enrollment,
        compatibleBatches: batchesResult.data || [],
      };
    })
  );

  return (
    <StudentProfile
      studentId={studentId}
      student={student}
      enrollmentsWithBatches={enrollmentsWithBatches}
    />
  );
}
