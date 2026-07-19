import Link from "next/link";
import { format, isBefore, startOfToday } from "date-fns";
import { Card, CardContent } from "@/shared/ui/card";
import { Button } from "@/shared/ui/button";
import { Badge } from "@/shared/ui/badge";
import type { EnquiryPipelineItemView } from "../types";

interface Props {
  pipeline: EnquiryPipelineItemView[];
}

export function PipelineView({ pipeline }: Props) {
  const today = startOfToday();

  // Filter based on status
  const followUps = pipeline.filter((item) => item.status === "FOLLOW_UP");
  const newEnquiries = pipeline.filter((item) => item.status === "NEW");

  // Group follow-ups
  const overdue = followUps.filter((item) => item.next_follow_up_at && isBefore(new Date(item.next_follow_up_at), today));
  const dueToday = followUps.filter((item) => item.next_follow_up_at && !isBefore(new Date(item.next_follow_up_at), today));

  return (
    <div className="space-y-10">
      
      {/* Needs Attention / Follow Ups */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-neutral-900">Needs Follow-up Today</h2>
          <span className="text-sm font-medium text-neutral-500">{followUps.length}</span>
        </div>

        {followUps.length === 0 ? (
          <p className="text-sm text-neutral-500 py-4">No follow-ups scheduled for today.</p>
        ) : (
          <div className="space-y-4">
            {overdue.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-red-600 uppercase tracking-wider mb-2">Overdue</h3>
                <div className="grid gap-3">
                  {overdue.map((item) => (
                    <PipelineCard key={item.enquiry_id} item={item} overdue />
                  ))}
                </div>
              </div>
            )}
            
            {dueToday.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-2 mt-4">Today</h3>
                <div className="grid gap-3">
                  {dueToday.map((item) => (
                    <PipelineCard key={item.enquiry_id} item={item} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </section>

      {/* New Enquiries */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-neutral-900">New Enquiries</h2>
          <span className="text-sm font-medium text-neutral-500">{newEnquiries.length}</span>
        </div>

        {newEnquiries.length === 0 ? (
          <p className="text-sm text-neutral-500 py-4">No new enquiries.</p>
        ) : (
          <div className="grid gap-3">
            {newEnquiries.map((item) => (
              <PipelineCard key={item.enquiry_id} item={item} />
            ))}
          </div>
        )}
      </section>

    </div>
  );
}

function PipelineCard({ item, overdue }: { item: EnquiryPipelineItemView; overdue?: boolean }) {
  return (
    <Card className={`overflow-hidden transition-colors hover:bg-neutral-50/50 ${overdue ? "border-red-200" : ""}`}>
      <CardContent className="p-4 flex items-center justify-between">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-neutral-900">{item.lead_name}</h3>
            {overdue && <Badge variant="destructive" className="h-5 px-1.5 text-[10px]">Overdue</Badge>}
            {item.status === "NEW" && <Badge variant="default" className="h-5 px-1.5 text-[10px]">New</Badge>}
          </div>
          <div className="text-sm text-neutral-500 flex items-center gap-2">
            <span>{item.course_name}</span>
            {item.next_follow_up_at && (
              <>
                <span>•</span>
                <span className={overdue ? "text-red-600" : ""}>
                  Follow-up: {format(new Date(item.next_follow_up_at), "MMM d, h:mm a")}
                </span>
              </>
            )}
          </div>
          {item.assigned_to && (
            <div className="text-xs text-neutral-400 mt-1">
              Assigned: {item.assigned_to}
            </div>
          )}
        </div>
        <div>
          <Button variant="outline" size="sm" render={<Link href={`/academy/admissions/${item.enquiry_id}`} />}>
            Open
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
