"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

export function ChatInput({ onSend, isLoading, disabled }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading && !disabled) {
      onSend(message.trim());
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-3 p-2 bg-gradient-to-r from-gray-50 to-gray-100 rounded-2xl shadow-sm border border-gray-200">
      <div className="relative flex-1">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about your tasks..."
          disabled={isLoading || disabled}
          rows={1}
          className={cn(
            "w-full resize-none rounded-xl border-0 bg-white px-4 py-3 shadow-inner",
            "text-sm text-gray-700 placeholder:text-gray-400 font-medium",
            "focus:outline-none focus:ring-2 focus:ring-purple-200",
            "disabled:cursor-not-allowed disabled:opacity-50",
            "transition-all duration-200"
          )}
        />
      </div>

      <Button
        type="submit"
        disabled={!message.trim() || isLoading || disabled}
        className={cn(
          "h-12 w-12 shrink-0 rounded-xl p-0 shadow-md",
          "bg-gradient-to-br from-purple-600 to-pink-600",
          "hover:from-purple-700 hover:to-pink-700",
          "disabled:opacity-50",
          "transition-all duration-200"
        )}
      >
        {isLoading ? (
          <Loader2 className="h-5 w-5 animate-spin text-white" />
        ) : (
          <Send className="h-5 w-5 text-white" />
        )}
      </Button>
    </form>
  );
}
