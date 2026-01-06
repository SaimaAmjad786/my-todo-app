"use client";

import { Calendar, Clock } from "lucide-react";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

interface DueDateSelectorProps {
  value: string | undefined;
  onChange: (value: string) => void;
}

export function DueDateSelector({ value, onChange }: DueDateSelectorProps) {
  return (
    <div className="relative">
      <Input
        type="datetime-local"
        value={value || ""}
        onChange={(e) => onChange(e.target.value)}
        className={cn(
          "pl-10 h-10 transition-all duration-200 border-gray-200 hover:border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        )}
        placeholder="Set due date and time"
      />
      <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
      {value && (
        <button
          type="button"
          onClick={() => onChange("")}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
        >
          ×
        </button>
      )}
    </div>
  );
}
