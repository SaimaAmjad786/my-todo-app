"use client";

import { Button } from "@/components/ui/button";
import { ClipboardList, Plus } from "lucide-react";

interface EmptyStateProps {
  onCreateClick: () => void;
}

export function EmptyState({ onCreateClick }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-200 p-12 text-center">
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-blue-100 to-purple-100">
        <ClipboardList className="h-8 w-8 text-blue-600" />
      </div>
      <h3 className="mt-4 text-lg font-semibold text-gray-900">No todos yet</h3>
      <p className="mt-2 text-sm text-gray-500">
        Get started by creating your first todo
      </p>
      <Button
        onClick={onCreateClick}
        className="mt-6 flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
      >
        <Plus className="h-4 w-4" />
        Create Todo
      </Button>
    </div>
  );
}
