"use client";

import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { MessageSquare, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatPanelProps {
  className?: string;
}

export function ChatPanel({ className }: ChatPanelProps) {
  const router = useRouter();

  return (
    <div className={cn("fixed top-4 left-1/2 -translate-x-1/2 z-50", className)}>
      <motion.button
        onClick={() => router.push("/chat")}
        className={cn(
          "relative flex items-center gap-2 px-5 py-2.5 rounded-full",
          "bg-gradient-to-r from-purple-600 via-pink-500 to-rose-500",
          "shadow-lg shadow-purple-500/30",
          "text-white font-semibold text-sm",
          "hover:shadow-xl hover:shadow-purple-500/40",
          "transition-shadow duration-300"
        )}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        animate={{
          boxShadow: [
            "0 10px 30px -10px rgba(168, 85, 247, 0.4)",
            "0 10px 30px -10px rgba(236, 72, 153, 0.4)",
            "0 10px 30px -10px rgba(168, 85, 247, 0.4)",
          ],
        }}
        transition={{
          boxShadow: {
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut",
          },
        }}
      >
        <motion.div
          animate={{ rotate: [0, 10, -10, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        >
          <MessageSquare className="h-4 w-4" />
        </motion.div>
        <span>AI Chatbot</span>
        <Sparkles className="h-3.5 w-3.5" />
      </motion.button>
    </div>
  );
}
