"use client";

import { ReactNode } from "react";
import Link from "next/link";
import { Sparkles } from "lucide-react";

interface AuthLayoutProps {
  children: ReactNode;
}

export default function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center px-4 py-12 overflow-hidden bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Background Orbs */}
      <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-200 rounded-full blur-3xl opacity-60" />
      <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-200 rounded-full blur-3xl opacity-60" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-pink-200 rounded-full blur-3xl opacity-40" />

      {/* Header */}
      <div className="relative mb-8 text-center">
        <Link href="/" className="inline-flex items-center gap-2 group">
          <div className="p-2 rounded-xl bg-gradient-to-br from-purple-600 to-pink-600 shadow-lg group-hover:scale-110 transition-transform">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <span className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Todo App
          </span>
        </Link>
        <p className="mt-3 text-gray-500">Organize your tasks efficiently</p>
      </div>

      {/* Card Container */}
      <div className="relative w-full max-w-md">{children}</div>
    </div>
  );
}
