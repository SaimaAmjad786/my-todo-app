"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Search, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface SearchInputProps {
  onSearch: (query: string) => void;
  initialValue?: string;
}

export function SearchInput({ onSearch, initialValue = "" }: SearchInputProps) {
  const [value, setValue] = useState(initialValue);

  useEffect(() => {
    const timeout = setTimeout(() => {
      onSearch(value);
    }, 300);
    return () => clearTimeout(timeout);
  }, [value, onSearch]);

  return (
    <div className="relative flex-1 max-w-md group">
      <div className="absolute inset-0 bg-gradient-to-r from-purple-200 via-pink-200 to-purple-200 rounded-2xl opacity-0 group-focus-within:opacity-20 blur-xl transition-opacity duration-300" />
      <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-purple-500 z-10 group-focus-within:text-pink-500 transition-colors duration-200" />
      <Input
        type="text"
        placeholder="Search your todos..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="h-12 pl-12 pr-12 text-base rounded-2xl border-2 border-purple-200 bg-gradient-to-r from-purple-50/50 to-pink-50/50 shadow-sm hover:shadow-md focus:bg-white focus:border-purple-400 focus:ring-4 focus:ring-purple-100 transition-all duration-200 relative"
      />
      {value && (
        <Button
          variant="ghost"
          size="icon"
          className="absolute right-2 top-1/2 h-8 w-8 -translate-y-1/2 z-10 rounded-xl hover:bg-red-100 hover:text-red-600 transition-all duration-200"
          onClick={() => setValue("")}
        >
          <X className="h-4 w-4" />
        </Button>
      )}
    </div>
  );
}
