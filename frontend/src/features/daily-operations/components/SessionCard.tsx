import Link from "next/link";
import { format, parseISO } from "date-fns";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/shared/ui/card";
import { Badge } from "@/shared/ui/badge";
import { buttonVariants } from "@/shared/ui/button";
import type { TodaySessionView } from "../types";

export function SessionCard({ session }: { session: TodaySessionView }) {
  const isSubmitted = !!session.attendance_submitted_at;
  
  const startTime = format(parseISO(session.starts_at), "h:mm a");
  const endTime = format(parseISO(session.ends_at), "h:mm a");

  return (
    <Card className="flex flex-col h-full transition-all hover:shadow-md border-neutral-200">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start gap-4">
          <div>
            <CardTitle className="text-lg font-semibold tracking-tight text-neutral-900">
              {session.course_title}
            </CardTitle>
            <CardDescription className="text-sm font-medium text-neutral-500 mt-1">
              {session.batch_name}
            </CardDescription>
          </div>
          <Badge variant={isSubmitted ? "secondary" : "default"} className={isSubmitted ? "bg-green-100 text-green-800 hover:bg-green-100" : ""}>
            {isSubmitted ? "Attendance Submitted" : "Attendance Pending"}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="pb-4 flex-grow">
        <div className="text-sm text-neutral-600 font-medium">
          {startTime} – {endTime}
        </div>
        <div className="text-sm text-neutral-500 mt-2">
          {session.assigned_student_count} Students
        </div>
      </CardContent>

      <CardFooter className="pt-0 border-t border-neutral-100 mt-auto">
        <Link 
          href={`/sessions/${session.session_id}`}
          className={buttonVariants({ variant: isSubmitted ? "outline" : "default", className: "w-full mt-4" })}
        >
          {isSubmitted ? "View Session" : "Open Session"}
        </Link>
      </CardFooter>
    </Card>
  );
}
