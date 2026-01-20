"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import type { Todo, Priority, Recurrence } from "@/types/api";
import { useCreateTodo, useUpdateTodo } from "@/hooks/useTodos";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { PrioritySelector } from "./PrioritySelector";
import { ApiError } from "@/lib/api-client";
import { Plus, Sparkles, Calendar, Repeat } from "lucide-react";
import { cn } from "@/lib/utils";

const todoSchema = z.object({
  title: z.string().min(1, "Title is required").max(255),
  description: z.string().max(5000).optional(),
  priority: z.enum(["high", "medium", "low"]),
  due_date: z.string().optional(),
  recurrence: z.enum(["none", "daily", "weekly", "monthly"]),
  tag_ids: z.array(z.string()).default([]),
});

type TodoFormData = z.infer<typeof todoSchema>;

interface TodoFormProps {
  todo?: Todo;
  onSuccess: () => void;
  onCancel: () => void;
}

export function TodoForm({ todo, onSuccess, onCancel }: TodoFormProps) {
  const [error, setError] = useState<string | null>(null);
  const createTodo = useCreateTodo();
  const updateTodo = useUpdateTodo();
  const isEditing = !!todo;

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    trigger,
    formState: { errors, isSubmitting },
  } = useForm<TodoFormData>({
    resolver: zodResolver(todoSchema),
    mode: "onChange",
    defaultValues: {
      title: todo?.title || "",
      description: todo?.description || "",
      priority: todo?.priority || "medium",
      due_date: todo?.due_date ? todo.due_date.slice(0, 10) : "",
      recurrence: todo?.recurrence || "none",
      tag_ids: [],
    },
  });

  const titleValue = watch("title");
  const priority = watch("priority");
  const recurrence = watch("recurrence");
  const canSubmit = titleValue.trim().length > 0 && !isSubmitting;

  const onSubmit = async (data: TodoFormData) => {
    setError(null);
    try {
      const payload: any = {
        title: data.title,
        description: data.description || undefined,
        priority: data.priority,
        recurrence: data.recurrence,
      };

      // Only add tag_ids when creating new todo (not editing)
      if (!isEditing) {
        payload.tag_ids = [];
      }

      // Only add due_date if it has a value
      if (data.due_date && data.due_date.trim()) {
        // Append time to make it a valid datetime (backend expects datetime)
        payload.due_date = `${data.due_date}T00:00:00`;
      }

      if (isEditing) {
        await updateTodo.mutateAsync({ todoId: todo.id, data: payload });
      } else {
        await createTodo.mutateAsync(payload);
      }
      onSuccess();
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-3 p-1">
      {error && (
        <div className="rounded-2xl bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 p-4 text-sm text-red-700 shadow-sm">
          <span className="font-medium">⚠️ {error}</span>
        </div>
      )}

      {/* Title */}
      <div className="space-y-2">
        <Label htmlFor="title" className="text-sm font-semibold text-gray-800 flex items-center gap-2">
          ✨ Task <span className="text-xs text-pink-500 font-normal">*required</span>
        </Label>
        <div className="relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-200 via-pink-200 to-purple-200 rounded-2xl opacity-0 group-focus-within:opacity-20 blur-xl transition-opacity duration-300" />
          <Input
            id="title"
            placeholder="What needs to be done? ✍️"
            className={cn(
              "h-10 text-sm rounded-2xl pl-3 pr-10 relative",
              "border-2 border-gray-200 bg-white shadow-sm",
              "focus:bg-white focus:border-purple-400 focus:ring-4 focus:ring-purple-100",
              "transition-all duration-200",
              errors.title && "border-red-300 bg-red-50 focus:border-red-400 focus:ring-red-100"
            )}
            {...register("title", { onChange: () => trigger("title") })}
          />
          {titleValue && !errors.title && (
            <Sparkles className="absolute right-4 top-1/2 -translate-y-1/2 h-5 w-5 text-purple-500 animate-pulse" />
          )}
        </div>
        {errors.title && (
          <p className="text-xs text-red-600 font-medium flex items-center gap-1">
            <span>❌</span> {errors.title.message}
          </p>
        )}
      </div>

      {/* Description */}
      <div className="space-y-2">
        <Label htmlFor="description" className="text-sm font-semibold text-gray-800 flex items-center gap-2">
          📝 Description <span className="text-xs text-gray-400 font-normal">(optional)</span>
        </Label>
        <Textarea
          id="description"
          placeholder="Add more details about your task..."
          className="min-h-[60px] resize-none text-sm rounded-2xl border-2 border-gray-200 bg-white shadow-sm px-3 py-2 focus:bg-white focus:border-purple-400 focus:ring-4 focus:ring-purple-100 transition-all duration-200"
          {...register("description")}
        />
      </div>

      {/* Priority */}
      <div className="space-y-2">
        <Label className="text-sm font-semibold text-gray-800 flex items-center gap-1">
          🎯 Priority
        </Label>
        <PrioritySelector
          value={priority}
          onChange={(value) => setValue("priority", value)}
        />
      </div>

      {/* Due Date */}
      <div className="space-y-2">
        <Label htmlFor="due_date" className="text-sm font-semibold text-gray-800 flex items-center gap-1">
          <Calendar className="w-4 h-4 text-purple-500" />
          Due Date <span className="text-xs text-gray-400 font-normal ml-1">(optional)</span>
        </Label>
        <Input
          id="due_date"
          type="date"
          className="h-9 text-sm rounded-xl border-2 border-gray-200 bg-white shadow-sm px-3 focus:bg-white focus:border-purple-400 focus:ring-4 focus:ring-purple-100 transition-all duration-200"
          {...register("due_date")}
        />
      </div>

      {/* Recurrence */}
      <div className="space-y-2">
        <Label htmlFor="recurrence" className="text-sm font-semibold text-gray-800 flex items-center gap-1">
          <Repeat className="w-4 h-4 text-purple-500" />
          Repeat
        </Label>
        <select
          id="recurrence"
          className="h-9 w-full text-sm rounded-xl border-2 border-gray-200 bg-white shadow-sm px-3 focus:bg-white focus:border-purple-400 focus:ring-4 focus:ring-purple-100 transition-all duration-200 cursor-pointer"
          {...register("recurrence")}
        >
          <option value="none">🚫 None</option>
          <option value="daily">📅 Daily</option>
          <option value="weekly">📆 Weekly</option>
          <option value="monthly">🗓️ Monthly</option>
        </select>
      </div>

      {/* Actions */}
      <div className="flex gap-3 pt-3">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          className="flex-1 h-10 rounded-xl border-2 border-gray-300 hover:bg-gray-100 hover:border-gray-400 text-sm font-medium text-gray-700 transition-all duration-200 shadow-sm"
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={!canSubmit}
          className={cn(
            "flex-1 h-10 text-sm font-bold rounded-xl transition-all duration-200 relative overflow-hidden",
            canSubmit
              ? "bg-gradient-to-r from-purple-600 via-pink-500 to-purple-600 shadow-lg shadow-purple-300 hover:shadow-xl hover:shadow-pink-300 hover:scale-[1.02] active:scale-[0.98] text-white"
              : "bg-gray-200 text-gray-400 cursor-not-allowed"
          )}
        >
          {isSubmitting ? (
            <div className="flex items-center gap-2">
              <div className="w-5 h-5 border-3 border-white/30 border-t-white rounded-full animate-spin" />
              <span>Processing...</span>
            </div>
          ) : isEditing ? (
            <span className="flex items-center gap-2">
              <Sparkles className="h-4 w-4" />
              Update Task
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <Plus className="h-5 w-5" />
              Create Task
            </span>
          )}
        </Button>
      </div>
    </form>
  );
}
