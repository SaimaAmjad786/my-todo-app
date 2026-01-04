"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ApiError } from "@/lib/api-client";
import { motion } from "framer-motion";
import { User, Mail, Lock, ArrowRight, ShieldCheck } from "lucide-react";

const signupSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  confirmPassword: z.string().min(1, "Please confirm your password"),
  name: z.string().optional(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type SignupFormData = z.infer<typeof signupSchema>;

export default function SignupPage() {
  const { signup } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
  });

  const onSubmit = async (data: SignupFormData) => {
    setError(null);
    setIsLoading(true);
    try {
      await signup(data.email, data.password, data.name);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.7, ease: "easeOut" }}
      className="relative bg-white/95 backdrop-blur-3xl rounded-[2.5rem] shadow-[0_25px_80px_-20px_rgba(147,51,234,0.4)] border-2 border-purple-100/60 overflow-hidden"
    >
      {/* Top Gradient Bar */}
      <motion.div
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-purple-600 via-pink-500 to-purple-600 origin-left"
      />

      {/* Decorative Corners */}
      <div className="absolute -top-24 -right-24 w-48 h-48 bg-gradient-to-br from-purple-300 to-pink-300 rounded-full blur-3xl opacity-50 animate-pulse" />
      <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-gradient-to-tr from-blue-300 to-purple-300 rounded-full blur-3xl opacity-40 animate-pulse" />

      {/* Header */}
      <div className="relative p-10 pb-4">
        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="text-4xl font-black bg-gradient-to-r from-gray-900 via-purple-800 to-gray-900 bg-clip-text text-transparent"
        >
          Create an account
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="text-gray-600 mt-3 font-medium"
        >
          Enter your details to get started
        </motion.p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit(onSubmit)} className="relative p-10 pt-4 space-y-5">
        {error && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="rounded-2xl bg-gradient-to-r from-red-50 to-pink-50 border-2 border-red-200 p-4 text-sm text-red-700 font-medium shadow-sm"
          >
            {error}
          </motion.div>
        )}

        {/* Name Field */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
          className="space-y-2.5"
        >
          <Label htmlFor="name" className="text-gray-800 font-semibold text-sm">Name (optional)</Label>
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-pink-400 rounded-2xl opacity-0 group-focus-within:opacity-20 blur-lg transition-all duration-300 -z-10 scale-105" />
            <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-purple-600 transition-all duration-300" />
            <Input
              id="name"
              placeholder="John Doe"
              {...register("name")}
              className="pl-12 h-14 rounded-2xl border-2 border-gray-200 bg-white shadow-sm focus:bg-white focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 text-base"
            />
          </div>
        </motion.div>

        {/* Email Field */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6, duration: 0.6 }}
          className="space-y-2.5"
        >
          <Label htmlFor="email" className="text-gray-800 font-semibold text-sm">Email</Label>
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-pink-400 rounded-2xl opacity-0 group-focus-within:opacity-20 blur-lg transition-all duration-300 -z-10 scale-105" />
            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-purple-600 transition-all duration-300" />
            <Input
              id="email"
              type="email"
              placeholder="john@example.com"
              {...register("email")}
              className="pl-12 h-14 rounded-2xl border-2 border-gray-200 bg-white shadow-sm focus:bg-white focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 text-base"
            />
          </div>
          {errors.email && (
            <p className="text-sm text-red-600 ml-1 font-medium">{errors.email.message}</p>
          )}
        </motion.div>

        {/* Password Field */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.7, duration: 0.6 }}
          className="space-y-2.5"
        >
          <Label htmlFor="password" className="text-gray-800 font-semibold text-sm">Password</Label>
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-pink-400 rounded-2xl opacity-0 group-focus-within:opacity-20 blur-lg transition-all duration-300 -z-10 scale-105" />
            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-purple-600 transition-all duration-300" />
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              {...register("password")}
              className="pl-12 h-14 rounded-2xl border-2 border-gray-200 bg-white shadow-sm focus:bg-white focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 text-base"
            />
          </div>
          {errors.password && (
            <p className="text-sm text-red-600 ml-1 font-medium">{errors.password.message}</p>
          )}
        </motion.div>

        {/* Confirm Password Field */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          className="space-y-2.5"
        >
          <Label htmlFor="confirmPassword" className="text-gray-800 font-semibold text-sm">Confirm Password</Label>
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-pink-400 rounded-2xl opacity-0 group-focus-within:opacity-20 blur-lg transition-all duration-300 -z-10 scale-105" />
            <ShieldCheck className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-purple-600 transition-all duration-300" />
            <Input
              id="confirmPassword"
              type="password"
              placeholder="••••••••"
              {...register("confirmPassword")}
              className="pl-12 h-14 rounded-2xl border-2 border-gray-200 bg-white shadow-sm focus:bg-white focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 text-base"
            />
          </div>
          {errors.confirmPassword && (
            <p className="text-sm text-red-600 ml-1 font-medium">{errors.confirmPassword.message}</p>
          )}
        </motion.div>

        {/* Submit Button */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9, duration: 0.6 }}
          className="pt-4"
        >
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full h-14 text-base font-bold bg-gradient-to-r from-purple-600 via-pink-500 to-purple-600 rounded-2xl shadow-[0_12px_45px_-15px_rgba(147,51,234,0.6)] hover:shadow-[0_20px_60px_-15px_rgba(147,51,234,0.7)] transition-all duration-300 hover:scale-[1.03] active:scale-[0.97]"
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <div className="w-5 h-5 border-3 border-white/30 border-t-white rounded-full animate-spin" />
                Creating account...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                Sign up
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </span>
            )}
          </Button>
        </motion.div>

        {/* Footer Link */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0 }}
          className="text-center text-gray-600 pt-4 font-medium"
        >
          Already have an account?{" "}
          <Link href="/signin" className="text-purple-600 font-bold hover:text-pink-600 transition-colors underline-offset-4 hover:underline">
            Sign in
          </Link>
        </motion.p>
      </form>
    </motion.div>
  );
}
