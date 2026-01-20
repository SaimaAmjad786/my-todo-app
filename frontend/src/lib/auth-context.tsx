"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { useRouter } from "next/navigation";
import { apiGet, apiPost, ApiError } from "./api-client";
import type { User, AuthResponse } from "@/types/api";

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  signin: (email: string, password: string) => Promise<void>;
  signout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_KEY = "access_token";

function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

function setStoredToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

function removeStoredToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const initAuth = async () => {
      const token = getStoredToken();
      if (token) {
        try {
          const userData = await apiGet<User>("/auth/me");
          setUser(userData);
        } catch {
          removeStoredToken();
        }
      }
      setIsLoading(false);
    };
    initAuth();
  }, []);

  const signup = async (email: string, password: string, name?: string) => {
    const response = await apiPost<AuthResponse>("/auth/signup", {
      email,
      password,
      name,
    });
    setStoredToken(response.access_token);
    setUser(response.user);
    router.push("/dashboard");
  };

  const signin = async (email: string, password: string) => {
    const response = await apiPost<AuthResponse>("/auth/signin", {
      email,
      password,
    });
    setStoredToken(response.access_token);
    setUser(response.user);
    router.push("/dashboard");
  };

  const signout = async () => {
    try {
      await apiPost("/auth/signout", {});
    } catch {
      // Ignore errors, proceed with local signout
    }
    removeStoredToken();
    setUser(null);
    router.push("/signin");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        signup,
        signin,
        signout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
