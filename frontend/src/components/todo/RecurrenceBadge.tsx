"use client";

import { Badge } from "@/components/ui/badge";
import { Repeat } from "lucide-react";
import type { Recurrence } from "@/types/api";

interface RecurrenceBadgeProps {
  recurrence: Recurrence;
}

const recurrenceLabels: Record<Recurrence, string> = {
  none: "None",
  daily: "Daily",
  weekly: "Weekly",
  monthly: "Monthly",
};

export function RecurrenceBadge({ recurrence }: RecurrenceBadgeProps) {
  if (recurrence === "none") return null;

  return (
    <Badge variant="secondary" className="text-xs flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 border border-purple-200 shadow-sm hover:shadow-md font-semibold">
      <Repeat className="h-3.5 w-3.5" />
      {recurrenceLabels[recurrence]}
    </Badge>
  );
}
