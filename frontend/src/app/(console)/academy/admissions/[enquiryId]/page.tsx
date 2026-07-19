import Link from "next/link";
import { notFound } from "next/navigation";
import { getEnquiryDetails } from "@/lib/api/academy/admissions";
import { EnquiryWorkspace } from "@/features/admissions/components/EnquiryWorkspace";
import { Button } from "@/shared/ui/button";
import { errorMessage } from "@/shared/types/api";

export const metadata = {
  title: "Enquiry Details",
};

interface PageProps {
  params: Promise<{
    enquiryId: string;
  }>;
}

export default async function EnquiryDetailsPage({ params }: PageProps) {
  const { enquiryId } = await params;
  
  const result = await getEnquiryDetails(enquiryId);

  if (result.error) {
    if (result.error.error?.code === "NOT_FOUND" || result.error.detail?.includes("not found")) {
      notFound();
    }
    return (
      <div className="p-8">
        <div className="bg-red-50 text-red-600 p-4 rounded-md">
          Failed to load enquiry: {errorMessage(result.error)}
        </div>
      </div>
    );
  }

  if (!result.data) {
    notFound();
  }

  const enquiry = result.data;

  // The actual lead details (name, phone, email) would typically be returned in EnquiryDetailsView. 
  // Let's assume they might not be part of the minimal EnquiryDetailsView in the DB right now, 
  // but if the backend provides them in the future we use them.
  // Wait, EnquiryPipelineItemView had lead_name, lead_phone. EnquiryDetailsView doesn't?
  // Let's check what we have in the query. EnquiryDetailsView has course_name, status, etc.
  // Wait, if EnquiryDetailsView lacks lead_name, we might need a workaround for now or we just display what we have.
  // In `EnquiryWorkspace` we accepted leadName, leadPhone, leadEmail. We will just pass empty strings if unavailable.
  // Let's check backend `EnquiryDetailsView` again. It only has `lead_id`, `course_id`, `course_name`, `status`, `source`, `assigned_to`, `next_follow_up_at`, `notes`, `created_at`.
  // Ideally it should have lead name. Since it doesn't, we will omit or fetch it separately.
  // Let's just use what we have for now.

  return (
    <div className="max-w-4xl p-6 lg:p-8">
      <div className="mb-6">
        <Button variant="ghost" className="-ml-4 text-neutral-500" render={<Link href="/academy/admissions" />}>
          ← Back to Admissions
        </Button>
      </div>
      
      <EnquiryWorkspace 
        enquiry={enquiry} 
        leadName={enquiry.lead_name}
        leadPhone={enquiry.lead_phone}
        leadEmail={enquiry.lead_email || undefined}
      />
    </div>
  );
}
