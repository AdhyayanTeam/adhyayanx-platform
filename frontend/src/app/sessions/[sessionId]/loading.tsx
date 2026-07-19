export default function LoadingSessionPage() {
  return (
    <main className="container max-w-4xl mx-auto py-8 px-4 sm:px-6">
      <div className="mb-6 animate-pulse">
        <div className="h-4 bg-neutral-200 rounded w-32 mb-4"></div>
        <div className="h-8 bg-neutral-200 rounded w-2/3 mb-2"></div>
        <div className="h-6 bg-neutral-200 rounded w-1/3 mb-4"></div>
        <div className="h-8 bg-neutral-200 rounded w-48 mt-4"></div>
      </div>
      <div className="border-t border-neutral-200 pt-6 mt-6 animate-pulse">
        <div className="h-6 bg-neutral-200 rounded w-32 mb-6"></div>
        <div className="bg-white rounded-lg border border-neutral-200 shadow-sm p-4">
          <div className="h-10 bg-neutral-200 rounded w-full mb-4"></div>
          <div className="h-10 bg-neutral-200 rounded w-full mb-4"></div>
          <div className="h-10 bg-neutral-200 rounded w-full"></div>
        </div>
      </div>
    </main>
  );
}
