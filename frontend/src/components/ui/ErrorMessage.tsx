"use client";

import { AlertCircle } from "lucide-react";
import { Button } from "./button";

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 rounded-lg border border-red-200 bg-red-50">
      <AlertCircle className="h-8 w-8 text-red-500 mb-3" />
      <p className="text-red-600 font-medium mb-3">{message}</p>
      {onRetry && (
        <Button variant="outline" size="sm" onClick={onRetry}>
          Try again
        </Button>
      )}
    </div>
  );
}
