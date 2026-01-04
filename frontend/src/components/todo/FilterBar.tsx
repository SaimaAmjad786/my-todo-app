"use client";

import type { TodoFilters, Priority } from "@/types/api";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { SortSelector } from "./SortSelector";

interface FilterBarProps {
  filters: TodoFilters;
  onFilterChange: (filters: Partial<TodoFilters>) => void;
}

export function FilterBar({ filters, onFilterChange }: FilterBarProps) {
  return (
    <div className="flex flex-wrap gap-3 items-center">
      {/* Status filter */}
      <div className="flex rounded-2xl border-2 border-purple-200 p-1.5 bg-gradient-to-r from-purple-50 to-pink-50 shadow-sm">
        <Button
          variant={filters.completed === undefined ? "default" : "ghost"}
          size="sm"
          className={filters.completed === undefined
            ? "h-9 px-5 text-sm font-bold rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-md"
            : "h-9 px-5 text-sm font-semibold rounded-xl hover:bg-white/80 text-gray-700 hover:text-purple-700"}
          onClick={() => onFilterChange({ completed: undefined })}
        >
          All
        </Button>
        <Button
          variant={filters.completed === false ? "default" : "ghost"}
          size="sm"
          className={filters.completed === false
            ? "h-9 px-5 text-sm font-bold rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-md"
            : "h-9 px-5 text-sm font-semibold rounded-xl hover:bg-white/80 text-gray-700 hover:text-purple-700"}
          onClick={() => onFilterChange({ completed: false })}
        >
          Active
        </Button>
        <Button
          variant={filters.completed === true ? "default" : "ghost"}
          size="sm"
          className={filters.completed === true
            ? "h-9 px-5 text-sm font-bold rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-md"
            : "h-9 px-5 text-sm font-semibold rounded-xl hover:bg-white/80 text-gray-700 hover:text-purple-700"}
          onClick={() => onFilterChange({ completed: true })}
        >
          Completed
        </Button>
      </div>
    </div>
  );
}
