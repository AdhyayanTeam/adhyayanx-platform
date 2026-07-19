import { getPipeline } from "@/lib/api/academy/admissions";
import { PipelineView } from "@/features/admissions/components/PipelineView";
import { errorMessage } from "@/shared/types/api";

export const metadata = {
  title: "Admissions Operations",
};

export default async function AdmissionsPage() {
  const result = await getPipeline();

  if (result.error || !result.data) {
    return (
      <div className="p-8">
        <div className="bg-red-50 text-red-600 p-4 rounded-md">
          Failed to load pipeline: {result.error ? errorMessage(result.error) : "No data"}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl p-6 lg:p-8">
      <header className="mb-10">
        <h1 className="text-2xl font-bold tracking-tight text-neutral-900">Admissions</h1>
        <p className="text-neutral-500 mt-1">Review enquiries and manage conversions.</p>
      </header>

      <PipelineView pipeline={result.data} />
    </div>
  );
}
