export default function BatchOperationsLoading() {
  return (
    <main className="container max-w-4xl mx-auto py-8 px-4 sm:px-6 animate-pulse">
      <div className="mb-8">
        <div className="h-4 w-48 bg-neutral-200 rounded mb-4"></div>
        <div className="h-9 w-3/4 bg-neutral-200 rounded mb-3"></div>
        <div className="h-7 w-1/2 bg-neutral-200 rounded mb-5"></div>
        
        <div className="flex items-center gap-2 mt-4">
          <div className="h-8 w-24 bg-neutral-200 rounded-md"></div>
          <div className="h-8 w-48 bg-neutral-200 rounded-md"></div>
        </div>
      </div>

      <hr className="border-neutral-200 mb-8" />

      <div className="space-y-12">
        <section>
          <div className="flex items-center justify-between mb-4">
            <div className="h-7 w-24 bg-neutral-200 rounded"></div>
            <div className="h-6 w-8 bg-neutral-200 rounded-full"></div>
          </div>

          <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
            <div className="divide-y divide-neutral-100">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="p-4 flex items-center justify-between">
                  <div>
                    <div className="h-5 w-40 bg-neutral-200 rounded mb-2"></div>
                    <div className="h-4 w-32 bg-neutral-100 rounded"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <hr className="border-neutral-200" />

        <section>
          <div className="h-7 w-48 bg-neutral-200 rounded mb-6"></div>
          
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-white border border-neutral-200 rounded-lg shadow-sm gap-4">
                <div className="min-w-48 shrink-0">
                  <div className="h-5 w-24 bg-neutral-200 rounded mb-2"></div>
                  <div className="h-4 w-16 bg-neutral-100 rounded"></div>
                </div>
                
                <div className="flex-grow max-w-md w-full">
                  <div className="flex justify-between mb-2">
                    <div className="h-4 w-24 bg-neutral-200 rounded"></div>
                    <div className="h-4 w-8 bg-neutral-200 rounded"></div>
                  </div>
                  <div className="w-full bg-neutral-100 rounded-full h-2">
                    <div className="bg-neutral-200 h-2 rounded-full w-2/3"></div>
                  </div>
                </div>
                
                <div className="shrink-0 h-8 w-16 bg-neutral-100 rounded"></div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
