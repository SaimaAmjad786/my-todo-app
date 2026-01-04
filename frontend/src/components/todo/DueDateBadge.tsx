"use client";

import { Badge } from "@/components/ui/badge";
import { Calendar } from "lucide-react";
import { format, isPast, isToday, isTomorrow } from "date-fns";
import { cn } from "@/lib/utils";

interface DueDateBadgeProps {
  dueDate: string;
  completed?: boolean;
}

export function DueDateBadge({ dueDate, completed }: DueDateBadgeProps) {
  const date = new Date(dueDate);
  const overdue = !completed && isPast(date) && !isToday(date);

  let displayText: string;
  if (isToday(date)) {
    displayText = "Today";
  } else if (isTomorrow(date)) {
    displayText = "Tomorrow";
  } else {
    displayText = format(date, "MMM d");
  }

  return (
    <Badge
      variant="secondary"
      className={cn(
        "text-xs flex items-center gap-1.5 px-3 py-1 font-semibold shadow-sm hover:shadow-md border",
        overdue
          ? "bg-gradient-to-r from-red-100 to-pink-100 text-red-700 border-red-200"
          : "bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-700 border-blue-200"
      )}
    >
      <Calendar className="h-3.5 w-3.5" />
      {displayText}
    </Badge>
  );
}
