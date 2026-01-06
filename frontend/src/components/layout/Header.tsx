"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { Sparkles, LogOut, User } from "lucide-react";

export function Header() {
  const { user, isAuthenticated, signout, isLoading } = useAuth();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-purple-100/50 bg-white/70 backdrop-blur-xl shadow-sm">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        {/* Logo */}
        <Link
          href={isAuthenticated ? "/dashboard" : "/"}
          className="flex items-center gap-2 group"
        >
          <div className="p-1.5 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 shadow-md group-hover:shadow-lg group-hover:scale-105 transition-all">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Todo App
          </span>
        </Link>

        {/* Navigation */}
        <nav className="flex items-center gap-3">
          {isLoading ? (
            <div className="h-9 w-24 animate-pulse rounded-xl bg-gradient-to-r from-purple-100 to-pink-100" />
          ) : isAuthenticated ? (
            <>
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-100">
                <User className="w-4 h-4 text-purple-500" />
                <span className="text-sm font-medium text-gray-700">
                  {user?.name || user?.email}
                </span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={signout}
                className="rounded-xl border-purple-200 hover:bg-purple-50 hover:border-purple-300 hover:text-purple-700 transition-all"
              >
                <LogOut className="w-4 h-4 mr-1.5" />
                Sign out
              </Button>
            </>
          ) : (
            <>
              <Link href="/signin">
                <Button
                  variant="ghost"
                  size="sm"
                  className="rounded-xl hover:bg-purple-50 hover:text-purple-700 transition-all"
                >
                  Sign in
                </Button>
              </Link>
              <Link href="/signup">
                <Button
                  size="sm"
                  className="rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-md shadow-purple-300/50 hover:shadow-lg hover:shadow-purple-400/50 transition-all"
                >
                  Sign up
                </Button>
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
