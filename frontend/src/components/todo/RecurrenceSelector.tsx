"use client";

import type { Recurrence } from "@/types/api";
import { Repeat } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { cn } from "@/lib/utils";

interface RecurrenceSelectorProps {
  value: Recurrence;
  onChange: (value: Recurrence) => void;
}

const options: { value: Recurrence; label: string; icon: string }[] = [
  { value: "none", label: "Does not repeat", icon: "—" },
  { value: "daily", label: "Daily", icon: "1D" },
  { value: "weekly", label: "Weekly", icon: "1W" },
  { value: "monthly", label: "Monthly", icon: "1M" },
];

export function RecurrenceSelector({ value, onChange }: RecurrenceSelectorProps) {
  return (
    <Select value={value} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => onChange(e.target.value as Recurrence)}>
      <SelectTrigger
        className={cn(
          "h-10 transition-all duration-200 border-gray-200 hover:border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        )}
      >
        <Repeat className="h-4 w-4 mr-2 text-gray-400" />
        <SelectValue placeholder="Select recurrence" />
      </SelectTrigger>
      <SelectContent>
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            <span className="flex items-center gap-2">
              <span className="w-8 h-6 rounded bg-gray-100 flex items-center justify-center text-xs font-medium text-gray-600">
                {option.icon}
              </span>
              {option.label}
            </span>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
