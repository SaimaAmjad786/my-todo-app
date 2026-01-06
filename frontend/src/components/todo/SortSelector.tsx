"use client";

import { Select } from "@/components/ui/select";

interface SortSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

const sortOptions = [
  { value: "-created_at", label: "Newest first" },
  { value: "created_at", label: "Oldest first" },
  { value: "due_date", label: "Due date (soonest)" },
  { value: "-due_date", label: "Due date (latest)" },
  { value: "-priority", label: "Priority (high first)" },
  { value: "priority", label: "Priority (low first)" },
  { value: "title", label: "Title (A-Z)" },
  { value: "-title", label: "Title (Z-A)" },
];

export function SortSelector({ value, onChange }: SortSelectorProps) {
  return (
    <Select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-44 h-9"
    >
      {sortOptions.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </Select>
  );
}
