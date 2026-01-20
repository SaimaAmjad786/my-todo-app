"use client";

import { MessageInfo, ToolCall } from "@/types/api";
import { cn } from "@/lib/utils";
import { Bot, User, Wrench } from "lucide-react";
import { motion } from "framer-motion";

interface ChatMessageProps {
  message: MessageInfo;
}

function ToolCallDisplay({ toolCall }: { toolCall: ToolCall }) {
  const isSuccess = toolCall.result?.success === true;

  return (
    <div className="mt-2 rounded-xl bg-white/80 backdrop-blur-sm p-3 text-sm border border-gray-200 shadow-sm">
      <div className="flex items-center gap-2 text-gray-600">
        <div className="p-1.5 rounded-lg bg-purple-100">
          <Wrench className="h-3.5 w-3.5 text-purple-600" />
        </div>
        <span className="font-semibold text-gray-700">{toolCall.tool}</span>
        <span
          className={cn(
            "ml-auto rounded-full px-2.5 py-1 text-xs font-medium shadow-sm",
            isSuccess ? "bg-gradient-to-r from-green-400 to-emerald-500 text-white" : "bg-gradient-to-r from-red-400 to-rose-500 text-white"
          )}
        >
          {isSuccess ? "Success" : "Failed"}
        </span>
      </div>
    </div>
  );
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={cn("flex gap-3", isUser && "flex-row-reverse")}
    >
      {/* Avatar */}
      <div
        className={cn(
          "flex h-10 w-10 shrink-0 items-center justify-center rounded-xl shadow-lg",
          isUser
            ? "bg-gradient-to-br from-purple-500 via-pink-500 to-rose-500"
            : "bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-600"
        )}
      >
        {isUser ? (
          <User className="h-5 w-5 text-white" />
        ) : (
          <Bot className="h-5 w-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div
        className={cn(
          "max-w-[80%] rounded-2xl px-5 py-3.5 shadow-md",
          isUser
            ? "bg-gradient-to-br from-purple-500 via-pink-500 to-rose-500 text-white"
            : "bg-white border border-gray-100 text-gray-800"
        )}
      >
        <p className="whitespace-pre-wrap text-sm leading-relaxed font-medium">{message.content}</p>

        {/* Tool Calls */}
        {isAssistant && message.tool_calls && message.tool_calls.length > 0 && (
          <div className="mt-3 space-y-2">
            {message.tool_calls.map((tc, idx) => (
              <ToolCallDisplay key={idx} toolCall={tc} />
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}
