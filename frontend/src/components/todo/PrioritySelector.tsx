"use client";

import type { Priority } from "@/types/api";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface PrioritySelectorProps {
  value: Priority;
  onChange: (priority: Priority) => void;
}

const priorities: { value: Priority; label: string; color: string; bgColor: string; hoverColor: string }[] = [
  { value: "high", label: "High", color: "text-red-700", bgColor: "bg-red-50", hoverColor: "hover:bg-red-100" },
  { value: "medium", label: "Medium", color: "text-orange-700", bgColor: "bg-orange-50", hoverColor: "hover:bg-orange-100" },
  { value: "low", label: "Low", color: "text-green-700", bgColor: "bg-green-50", hoverColor: "hover:bg-green-100" },
];

export function PrioritySelector({ value, onChange }: PrioritySelectorProps) {
  return (
    <div className="flex gap-2">
      {priorities.map((priority) => {
        const isSelected = value === priority.value;
        return (
          <button
            key={priority.value}
            type="button"
            onClick={() => onChange(priority.value)}
            className={cn(
              "flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200",
              "border border-transparent",
              isSelected
                ? `${priority.bgColor} ${priority.color} border-current shadow-sm`
                : `bg-gray-50 text-gray-600 hover:bg-gray-100 border-gray-200`,
              "focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-blue-500"
            )}
          >
            <span
              className={cn(
                "h-2 w-2 rounded-full",
                isSelected
                  ? priority.value === "high" ? "bg-red-500"
                    : priority.value === "medium" ? "bg-orange-500"
                    : "bg-green-500"
                  : "bg-gray-400"
              )}
            />
            {priority.label}
          </button>
        );
      })}
    </div>
  );
}
