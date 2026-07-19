import { format } from "date-fns";
import { getTodaysSessions } from "@/lib/api/academy/delivery";
import { SessionCard } from "@/features/daily-operations/components/SessionCard";
import { errorMessage } from "@/shared/types/api";

export default async function TodayOperationsPage() {
  const result = await getTodaysSessions();
  
  return (
    <main className="container max-w-5xl mx-auto py-8 px-4 sm:px-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-neutral-900">Today's Classes</h1>
          <p className="text-neutral-500 mt-1">Good morning. Here is what is happening at your institute today.</p>
        </div>
        <div className="text-sm font-medium text-neutral-600 bg-neutral-100 px-4 py-2 rounded-md">
          {format(new Date(), "MMMM d, yyyy")}
        </div>
      </div>

      {result.error && (
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md mb-8">
          Failed to load today's sessions: {errorMessage(result.error)}
        </div>
      )}

      {result.data && result.data.length === 0 && (
        <div className="text-center py-20 bg-neutral-50 rounded-lg border border-neutral-200 border-dashed">
          <h3 className="text-lg font-medium text-neutral-900">No classes scheduled</h3>
          <p className="text-neutral-500 mt-1">There are no sessions scheduled for today.</p>
        </div>
      )}

      {result.data && result.data.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {result.data.map((session) => (
            <SessionCard key={session.session_id} session={session} />
          ))}
        </div>
      )}
    </main>
  );
}
