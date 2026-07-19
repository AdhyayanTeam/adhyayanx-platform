import Link from "next/link";
import { format, parseISO } from "date-fns";
import { getBatchOverview, getBatchRoster, getBatchAttendanceSummary } from "@/lib/api/academy/delivery";
import { buttonVariants } from "@/shared/ui/button";

export default async function BatchOperationsPage({ params }: { params: { batchId: string } }) {
  const { batchId } = params;

  const [overviewRes, rosterRes, historyRes] = await Promise.all([
    getBatchOverview(batchId),
    getBatchRoster(batchId),
    getBatchAttendanceSummary(batchId),
  ]);

  if (overviewRes.error || !overviewRes.data) {
    return (
      <main className="container max-w-4xl mx-auto py-8 px-4 sm:px-6">
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md">
          Batch not found or an error occurred.
        </div>
        <Link href="/academy/today" className={buttonVariants({ variant: "outline", className: "mt-4" })}>
          Back to Today's Operations
        </Link>
      </main>
    );
  }

  const overview = overviewRes.data;
  const roster = rosterRes.data || [];
  const history = historyRes.data || [];

  return (
    <main className="container max-w-4xl mx-auto py-8 px-4 sm:px-6">
      <div className="mb-8">
        <Link href="/academy/today" className={buttonVariants({ variant: "link", className: "px-0 text-neutral-500 mb-2" })}>
          ← Back to Today's Operations
        </Link>
        <h1 className="text-3xl font-bold tracking-tight text-neutral-900">{overview.course_title}</h1>
        <p className="text-xl font-medium text-neutral-600 mt-1">{overview.batch_name}</p>
        
        <div className="flex items-center gap-2 mt-4 text-sm font-medium text-neutral-600">
          <span className="bg-neutral-100 px-3 py-1.5 rounded-md">
            {overview.assigned_student_count} Students
          </span>
          {overview.next_session_starts_at ? (
            <span className="bg-blue-50 text-blue-700 px-3 py-1.5 rounded-md border border-blue-100">
              Next class: {format(parseISO(overview.next_session_starts_at), "MMM d, h:mm a")}
            </span>
          ) : (
            <span className="bg-neutral-100 px-3 py-1.5 rounded-md">
              No upcoming session scheduled
            </span>
          )}
        </div>
      </div>

      <hr className="border-neutral-200 mb-8" />

      <div className="space-y-12">
        {/* Roster Section */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold tracking-tight text-neutral-900">Students</h2>
            <span className="text-sm font-medium text-neutral-500 bg-neutral-100 px-2.5 py-0.5 rounded-full">
              {roster.length}
            </span>
          </div>

          {roster.length === 0 ? (
            <div className="bg-neutral-50 border border-neutral-200 border-dashed rounded-lg p-8 text-center">
              <p className="text-neutral-500">No students are currently assigned to this batch.</p>
            </div>
          ) : (
            <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
              <div className="divide-y divide-neutral-100">
                {roster.map((student) => (
                  <div key={student.student_id} className="p-4 flex items-center justify-between hover:bg-neutral-50 transition-colors">
                    <div className="font-medium text-neutral-900">{student.name}</div>
                    <div className="text-sm text-neutral-500">{student.email}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>

        <hr className="border-neutral-200" />

        {/* Attendance History Section */}
        <section>
          <h2 className="text-xl font-semibold tracking-tight text-neutral-900 mb-6">Attendance History</h2>
          
          {history.length === 0 ? (
            <div className="bg-neutral-50 border border-neutral-200 border-dashed rounded-lg p-8 text-center">
              <p className="text-neutral-500">No completed attendance records yet.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {history.map((session) => {
                const isPending = !session.attendance_submitted_at;
                const total = session.present_count + session.absent_count;
                const percentage = total > 0 ? (session.present_count / total) * 100 : 0;
                
                return (
                  <div key={session.session_id} className="group flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-white border border-neutral-200 rounded-lg shadow-sm hover:border-neutral-300 transition-colors gap-4">
                    <div className="min-w-48 shrink-0">
                      <div className="font-medium text-neutral-900">
                        {format(parseISO(session.starts_at), "MMM d, yyyy")}
                      </div>
                      <div className="text-sm text-neutral-500">
                        {format(parseISO(session.starts_at), "h:mm a")}
                      </div>
                    </div>
                    
                    <div className="flex-grow max-w-md w-full">
                      {isPending ? (
                        <div className="flex items-center gap-2 text-yellow-600 bg-yellow-50 px-3 py-1.5 rounded-md border border-yellow-100 w-fit">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                          <span className="text-sm font-medium">Attendance pending</span>
                        </div>
                      ) : (
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="font-medium text-neutral-700">{session.present_count} / {total} present</span>
                            <span className="text-neutral-500">{Math.round(percentage)}%</span>
                          </div>
                          <div className="w-full bg-neutral-100 rounded-full h-2 overflow-hidden">
                            <div 
                              className="bg-green-500 h-2 rounded-full transition-all duration-500 ease-out" 
                              style={{ width: `${percentage}%` }}
                            ></div>
                          </div>
                        </div>
                      )}
                    </div>
                    
                    <div className="shrink-0 flex items-center h-full">
                      <Link 
                        href={`/sessions/${session.session_id}`} 
                        className={buttonVariants({ variant: "ghost", size: "sm", className: "text-neutral-500 opacity-0 group-hover:opacity-100 transition-opacity focus-within:opacity-100" })}
                      >
                        View
                      </Link>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
