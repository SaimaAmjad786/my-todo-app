"use client";

import { Badge } from "@/components/ui/badge";
import type { Priority } from "@/types/api";
import { cn } from "@/lib/utils";

interface PriorityBadgeProps {
  priority: Priority;
  className?: string;
}

const priorityConfig = {
  high: {
    label: "High",
    className: "bg-gradient-to-r from-red-100 to-pink-100 text-red-700 border border-red-200 shadow-sm hover:shadow-md font-semibold",
  },
  medium: {
    label: "Medium",
    className: "bg-gradient-to-r from-yellow-100 to-amber-100 text-amber-700 border border-amber-200 shadow-sm hover:shadow-md font-semibold",
  },
  low: {
    label: "Low",
    className: "bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 border border-green-200 shadow-sm hover:shadow-md font-semibold",
  },
};

export function PriorityBadge({ priority, className }: PriorityBadgeProps) {
  const config = priorityConfig[priority];

  return (
    <Badge variant="secondary" className={cn("text-xs px-3 py-1", config.className, className)}>
      {config.label}
    </Badge>
  );
}
