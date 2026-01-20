"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { MessageSquare, ArrowLeft, Trash2, Plus, Sparkles, Bot } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ChatMessage } from "@/components/chat/ChatMessage";
import { ChatInput } from "@/components/chat/ChatInput";
import { apiPost, apiDelete } from "@/lib/api-client";
import { ChatRequest, ChatResponse, MessageInfo } from "@/types/api";

const CHAT_STORAGE_KEY = "chat_messages";
const CONV_STORAGE_KEY = "chat_conversation_id";

export default function ChatPage() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const [messages, setMessages] = useState<MessageInfo[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load messages from localStorage on mount
  useEffect(() => {
    const savedMessages = localStorage.getItem(CHAT_STORAGE_KEY);
    const savedConvId = localStorage.getItem(CONV_STORAGE_KEY);
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch {
        // Ignore parse errors
      }
    }
    if (savedConvId) {
      setConversationId(savedConvId);
    }
  }, []);

  // Save messages to localStorage when they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(messages));
    }
  }, [messages]);

  // Save conversationId to localStorage when it changes
  useEffect(() => {
    if (conversationId) {
      localStorage.setItem(CONV_STORAGE_KEY, conversationId);
    }
  }, [conversationId]);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/signin");
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = useCallback(
    async (content: string) => {
      if (!content.trim()) return;

      const userMessage: MessageInfo = {
        id: `temp-${Date.now()}`,
        role: "user",
        content,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage]);
      setError(null);
      setIsLoading(true);

      try {
        const request: ChatRequest = {
          message: content,
          conversation_id: conversationId || undefined,
        };

        const response = await apiPost<ChatResponse>("/chat", request);

        if (!conversationId) {
          setConversationId(response.conversation_id);
        }

        const assistantMessage: MessageInfo = {
          id: `response-${Date.now()}`,
          role: "assistant",
          content: response.response,
          tool_calls: response.tool_calls.length > 0 ? response.tool_calls : undefined,
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to send message");
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId]
  );

  const handleNewConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
    localStorage.removeItem(CHAT_STORAGE_KEY);
    localStorage.removeItem(CONV_STORAGE_KEY);
  }, []);

  const handleClearConversation = useCallback(async () => {
    if (conversationId) {
      try {
        await apiDelete(`/chat/conversations/${conversationId}`);
      } catch {
        // Ignore
      }
    }
    handleNewConversation();
  }, [conversationId, handleNewConversation]);

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="h-16 w-16 animate-spin rounded-full border-4 border-purple-500 border-t-transparent" />
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-10 w-72 h-72 bg-purple-300/30 rounded-full blur-3xl"
          animate={{ x: [0, 50, 0], y: [0, 30, 0] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute bottom-20 right-10 w-96 h-96 bg-pink-300/30 rounded-full blur-3xl"
          animate={{ x: [0, -30, 0], y: [0, -50, 0] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      {/* Header */}
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="relative bg-gradient-to-r from-purple-600 via-pink-500 to-rose-500 px-4 py-4 shadow-xl"
      >
        <div className="container mx-auto flex items-center justify-between max-w-4xl">
          <div className="flex items-center gap-3">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                variant="ghost"
                onClick={() => router.push("/dashboard")}
                className="text-white/90 hover:bg-white/20 hover:text-white gap-2"
              >
                <ArrowLeft className="h-5 w-5" />
                <span className="font-bold text-white">Back to Dashboard</span>
              </Button>
            </motion.div>
            <div className="flex items-center gap-2">
              <motion.div
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              >
                <Bot className="h-7 w-7 text-white" />
              </motion.div>
              <span className="text-xl font-bold text-white">AI Chatbot</span>
              <Sparkles className="h-4 w-4 text-yellow-300" />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
              <Button
                variant="ghost"
                size="icon"
                onClick={handleNewConversation}
                className="text-white/90 hover:bg-white/20 hover:text-white rounded-xl"
                title="New conversation"
              >
                <Plus className="h-5 w-5" />
              </Button>
            </motion.div>
            <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
              <Button
                variant="ghost"
                size="icon"
                onClick={handleClearConversation}
                className="text-white/90 hover:bg-white/20 hover:text-white rounded-xl"
                title="Clear conversation"
              >
                <Trash2 className="h-5 w-5" />
              </Button>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Chat Area */}
      <div className="container mx-auto max-w-4xl p-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-white/60 overflow-hidden"
          style={{ height: "calc(100vh - 140px)" }}
        >
          {/* Messages */}
          <div className="h-[calc(100%-80px)] overflow-y-auto p-6">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", duration: 0.5 }}
                  className="relative"
                >
                  <motion.div
                    className="p-8 rounded-3xl bg-gradient-to-br from-purple-500 via-pink-500 to-rose-500 mb-6 shadow-2xl"
                    animate={{
                      boxShadow: [
                        "0 25px 50px -12px rgba(168, 85, 247, 0.4)",
                        "0 25px 50px -12px rgba(236, 72, 153, 0.4)",
                        "0 25px 50px -12px rgba(168, 85, 247, 0.4)",
                      ]
                    }}
                    transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                  >
                    <motion.div
                      animate={{ rotate: [0, 10, -10, 0] }}
                      transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                    >
                      <Bot className="h-16 w-16 text-white" />
                    </motion.div>
                  </motion.div>
                  <motion.div
                    className="absolute -top-2 -right-2"
                    animate={{ scale: [1, 1.2, 1], rotate: [0, 15, 0] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                  >
                    <Sparkles className="h-8 w-8 text-yellow-400" />
                  </motion.div>
                </motion.div>
                <motion.h2
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="text-3xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 bg-clip-text text-transparent mb-3"
                >
                  AI Task Assistant
                </motion.h2>
                <motion.p
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                  className="text-gray-500 mb-8 text-lg"
                >
                  I can help you manage your tasks easily!
                </motion.p>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="flex flex-wrap gap-3 justify-center max-w-lg"
                >
                  <motion.span whileHover={{ scale: 1.05, y: -2 }} className="px-5 py-2.5 bg-purple-50 text-purple-700 rounded-full text-sm font-semibold border border-purple-200 shadow-sm cursor-default">
                    Add a new task
                  </motion.span>
                  <motion.span whileHover={{ scale: 1.05, y: -2 }} className="px-5 py-2.5 bg-pink-50 text-pink-700 rounded-full text-sm font-semibold border border-pink-200 shadow-sm cursor-default">
                    Show my tasks
                  </motion.span>
                  <motion.span whileHover={{ scale: 1.05, y: -2 }} className="px-5 py-2.5 bg-blue-50 text-blue-700 rounded-full text-sm font-semibold border border-blue-200 shadow-sm cursor-default">
                    Update task
                  </motion.span>
                  <motion.span whileHover={{ scale: 1.05, y: -2 }} className="px-5 py-2.5 bg-green-50 text-green-700 rounded-full text-sm font-semibold border border-green-200 shadow-sm cursor-default">
                    Complete task
                  </motion.span>
                </motion.div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((msg) => (
                  <ChatMessage key={msg.id} message={msg} />
                ))}
                {isLoading && (
                  <div className="flex gap-3">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl shadow-lg bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-600">
                      <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    </div>
                    <div className="rounded-2xl bg-white border border-gray-100 px-5 py-4 shadow-md">
                      <div className="flex gap-1.5">
                        <div className="h-2.5 w-2.5 animate-bounce rounded-full bg-purple-400" />
                        <div className="h-2.5 w-2.5 animate-bounce rounded-full bg-pink-400" style={{ animationDelay: "0.15s" }} />
                        <div className="h-2.5 w-2.5 animate-bounce rounded-full bg-rose-400" style={{ animationDelay: "0.3s" }} />
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}

            {error && (
              <div className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-gray-100 p-4 bg-white/50">
            <ChatInput onSend={handleSend} isLoading={isLoading} />
          </div>
        </motion.div>
      </div>
    </div>
  );
}
