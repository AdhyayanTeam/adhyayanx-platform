import Link from "next/link";
import { format, parseISO } from "date-fns";
import { getSessionAttendance, getTodaysSessions } from "@/lib/api/academy/delivery";
import { AttendanceForm } from "@/features/attendance/components/AttendanceForm";
import { errorMessage } from "@/shared/types/api";
import { Button, buttonVariants } from "@/shared/ui/button";

export default async function SessionPage({ params }: { params: { sessionId: string } }) {
  const { sessionId } = params;

  const [attendanceRes, sessionsRes] = await Promise.all([
    getSessionAttendance(sessionId),
    getTodaysSessions(),
  ]);

  const students = attendanceRes.data || [];
  const sessionData = (sessionsRes.data || []).find(s => s.session_id === sessionId);

  if (!sessionData) {
    return (
      <main className="container max-w-4xl mx-auto py-8 px-4 sm:px-6">
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md">
          Session not found or an error occurred.
        </div>
        <Link href="/" className={buttonVariants({ variant: "outline", className: "mt-4" })}>
          Back to Today's Operations
        </Link>
      </main>
    );
  }

  const isSubmitted = !!sessionData.attendance_submitted_at;
  const startTime = format(parseISO(sessionData.starts_at), "h:mm a");
  const endTime = format(parseISO(sessionData.ends_at), "h:mm a");
  const displayDate = format(parseISO(sessionData.starts_at), "MMMM d, yyyy");
  
  const presentCount = students.filter(s => s.status === "PRESENT").length;
  const absentCount = students.filter(s => s.status === "ABSENT").length;

  return (
    <main className="container max-w-4xl mx-auto py-8 px-4 sm:px-6">
      <div className="mb-6">
        <Link href="/" className={buttonVariants({ variant: "link", className: "px-0 text-neutral-500 mb-2" })}>
          ← Back to Today's Operations
        </Link>
        <h1 className="text-3xl font-bold tracking-tight text-neutral-900">{sessionData.course_title}</h1>
        <p className="text-lg font-medium text-neutral-500 mt-1">{sessionData.batch_name}</p>
        <div className="text-sm font-medium text-neutral-600 bg-neutral-100 px-3 py-1.5 rounded-md inline-block mt-4">
          {displayDate} • {startTime} – {endTime}
        </div>
      </div>

      <div className="border-t border-neutral-200 pt-6 mt-6">
        <h2 className="text-xl font-semibold tracking-tight text-neutral-900 mb-4">
          Attendance
        </h2>
        
        {isSubmitted ? (
          <div className="space-y-6">
            <div className="bg-green-50 border border-green-200 p-6 rounded-lg flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 text-green-800 font-semibold text-lg">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                  Attendance Submitted
                </div>
                <div className="text-green-700 text-sm mt-1">
                  {students.length} students • {presentCount} present • {absentCount} absent
                </div>
              </div>
              <Button variant="outline" className="bg-white hover:bg-neutral-50 text-neutral-700">
                Edit Attendance
              </Button>
            </div>

            <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
              <div className="divide-y divide-neutral-100">
                {students.map((student) => (
                  <div key={student.student_id} className="p-4 flex items-center justify-between">
                    <div>
                      <div className="font-medium text-neutral-900">{student.name}</div>
                      <div className="text-sm text-neutral-500">{student.email}</div>
                    </div>
                    <div className="text-sm font-medium text-neutral-600 bg-neutral-100 px-4 py-1.5 rounded-md">
                      {student.status === "PRESENT" ? "Present" : "Absent"}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <AttendanceForm sessionId={sessionId} initialRoster={students} />
        )}
      </div>
    </main>
  );
}
