import Link from "next/link";
import { format } from "date-fns";
import type { EnquiryDetailsView } from "../types";
import { RecordFollowUpDialog } from "./RecordFollowUpDialog";
import { ConfirmAdmissionDialog } from "./ConfirmAdmissionDialog";
import { MarkLostDialog } from "./MarkLostDialog";
import { Button } from "@/shared/ui/button";

interface Props {
  enquiry: EnquiryDetailsView;
  leadName?: string;
  leadPhone?: string;
  leadEmail?: string;
}

export function EnquiryWorkspace({ enquiry, leadName, leadPhone, leadEmail }: Props) {
  const isTerminal = enquiry.status === "ADMITTED" || enquiry.status === "LOST";

  return (
    <div className="max-w-3xl space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-neutral-900">{leadName || "Unknown Prospect"}</h1>
        <p className="text-neutral-500">{enquiry.course_name}</p>
      </div>

      {/* Terminal State Banners */}
      {enquiry.status === "ADMITTED" && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-green-900 mb-1">Admission completed</h2>
          <p className="text-sm text-green-800">
            {leadName || "This student"} is now enrolled in {enquiry.course_name}.
          </p>
          {enquiry.student_id && (
            <div className="mt-4">
              <Button size="sm" render={<Link href={`/academy/students/${enquiry.student_id}`} />}>
                View Student
              </Button>
            </div>
          )}
        </div>
      )}

      {enquiry.status === "LOST" && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-red-900 mb-1">Enquiry closed as lost</h2>
          {enquiry.notes && (
            <div className="mt-4">
              <h3 className="text-xs font-semibold text-red-800 uppercase tracking-wider mb-1">Reason</h3>
              <p className="text-sm text-red-900 whitespace-pre-wrap">{enquiry.notes}</p>
            </div>
          )}
        </div>
      )}

      {/* Info Grid */}
      <div className="grid sm:grid-cols-2 gap-8 py-6 border-y border-neutral-200">
        <div className="space-y-4">
          <div>
            <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-1">Phone</h3>
            <p className="text-sm font-medium text-neutral-900">{leadPhone || "—"}</p>
          </div>
          <div>
            <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-1">Email</h3>
            <p className="text-sm font-medium text-neutral-900">{leadEmail || "—"}</p>
          </div>
        </div>
        <div className="space-y-4">
          <div>
            <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-1">Source</h3>
            <p className="text-sm font-medium text-neutral-900">{enquiry.source}</p>
          </div>
          <div>
            <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-1">Assigned</h3>
            <p className="text-sm font-medium text-neutral-900">{enquiry.assigned_to || "Unassigned"}</p>
          </div>
        </div>
      </div>

      {/* Active Pipeline details */}
      {!isTerminal && (
        <div className="space-y-6">
          {enquiry.next_follow_up_at && (
            <div>
              <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-1">Next follow-up</h3>
              <p className="text-sm font-medium text-neutral-900">
                {format(new Date(enquiry.next_follow_up_at), "MMMM d, yyyy 'at' h:mm a")}
              </p>
            </div>
          )}

          {enquiry.notes && (
            <div>
              <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-1">Latest Notes</h3>
              <div className="bg-neutral-50 p-4 rounded-md">
                <p className="text-sm text-neutral-700 whitespace-pre-wrap">{enquiry.notes}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      {!isTerminal && (
        <div className="flex flex-col sm:flex-row items-center gap-4 pt-6 border-t border-neutral-200">
          <div className="flex items-center gap-2 w-full sm:w-auto">
            <RecordFollowUpDialog enquiryId={enquiry.enquiry_id} />
          </div>
          <div className="flex items-center gap-2 w-full sm:w-auto sm:ml-auto">
            <MarkLostDialog enquiryId={enquiry.enquiry_id} />
            <ConfirmAdmissionDialog 
              enquiryId={enquiry.enquiry_id} 
              studentName={leadName || "Prospect"} 
              courseName={enquiry.course_name} 
            />
          </div>
        </div>
      )}
    </div>
  );
}
