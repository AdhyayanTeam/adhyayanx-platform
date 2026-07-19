export default function LoadingDashboard() {
  return (
    <main className="container max-w-5xl mx-auto py-8 px-4 sm:px-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div className="animate-pulse">
          <div className="h-8 bg-neutral-200 rounded w-48 mb-2"></div>
          <div className="h-4 bg-neutral-200 rounded w-64"></div>
        </div>
        <div className="h-8 bg-neutral-100 rounded w-32 animate-pulse"></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-48 bg-neutral-100 rounded-xl border border-neutral-200 animate-pulse"></div>
        ))}
      </div>
    </main>
  );
}
