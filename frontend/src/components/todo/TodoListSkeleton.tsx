"use client";

export function TodoListSkeleton() {
  return (
    <div className="space-y-3">
      {[1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          className="rounded-lg border bg-white p-4 animate-pulse"
        >
          <div className="flex items-start gap-3">
            <div className="h-5 w-5 rounded bg-gray-200" />
            <div className="flex-1 space-y-2">
              <div className="h-5 w-3/4 bg-gray-200 rounded" />
              <div className="flex gap-2">
                <div className="h-5 w-16 bg-gray-200 rounded" />
                <div className="h-5 w-20 bg-gray-200 rounded" />
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
