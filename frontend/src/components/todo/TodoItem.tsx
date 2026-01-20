"use client";

import { useState } from "react";
import type { Todo } from "@/types/api";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { PriorityBadge } from "./PriorityBadge";
import { DueDateBadge } from "./DueDateBadge";
import { RecurrenceBadge } from "./RecurrenceBadge";
import { DeleteConfirmDialog } from "./DeleteConfirmDialog";
import { Pencil, Trash2, ChevronDown, ChevronUp, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface TodoItemProps {
  todo: Todo;
  onToggleComplete: (todo: Todo) => void;
  onDelete: (todoId: string) => void;
  onEdit: (todo: Todo) => void;
}

export function TodoItem({ todo, onToggleComplete, onDelete, onEdit }: TodoItemProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  const handleDelete = () => {
    onDelete(todo.id);
    setIsDeleteDialogOpen(false);
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        transition={{ duration: 0.2 }}
        className={cn(
          "group relative rounded-2xl border-2 bg-white backdrop-blur-sm p-5 shadow-lg transition-all duration-300",
          "hover:shadow-2xl hover:shadow-purple-300/40 hover:border-purple-300 hover:-translate-y-1",
          todo.completed && "bg-gradient-to-r from-green-50 to-emerald-50 border-green-300"
        )}
      >
        {/* Left accent bar */}
        <div className={cn(
          "absolute left-0 top-0 bottom-0 w-1.5 rounded-l-2xl transition-colors",
          todo.priority === "high" && "bg-gradient-to-b from-red-500 to-pink-500",
          todo.priority === "medium" && "bg-gradient-to-b from-amber-500 to-orange-500",
          todo.priority === "low" && "bg-gradient-to-b from-blue-500 to-cyan-500",
          todo.completed && "bg-gradient-to-b from-green-500 to-emerald-500"
        )} />

        <div className="flex items-start gap-4 pl-2">
          {/* Checkbox */}
          <div className="pt-1">
            <div
              onClick={() => onToggleComplete(todo)}
              className={cn(
                "h-7 w-7 rounded-full border-2 flex items-center justify-center cursor-pointer transition-all duration-300 hover:scale-110",
                todo.completed
                  ? "bg-gradient-to-br from-green-500 to-emerald-600 border-green-500 shadow-lg shadow-green-300/50"
                  : "border-gray-400 hover:border-purple-500 hover:shadow-lg hover:shadow-purple-200 hover:bg-purple-50"
              )}
            >
              {todo.completed && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 500 }}
                >
                  <CheckCircle2 className="h-5 w-5 text-white" />
                </motion.div>
              )}
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1">
                {/* Title */}
                <h3
                  className={cn(
                    "font-bold text-lg text-gray-900 transition-all",
                    todo.completed && "line-through text-gray-500"
                  )}
                >
                  {todo.title}
                </h3>

                {/* Badges row */}
                <div className="mt-3 flex flex-wrap items-center gap-2">
                  <PriorityBadge priority={todo.priority} />
                  {todo.due_date && <DueDateBadge dueDate={todo.due_date} completed={todo.completed} />}
                  {todo.recurrence !== "none" && <RecurrenceBadge recurrence={todo.recurrence} />}
                  {todo.tags?.map((tag) => (
                    <Badge
                      key={tag.id}
                      variant="secondary"
                      className="text-xs px-3 py-1 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 border-0 shadow-sm font-semibold"
                    >
                      {tag.name}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Action buttons */}
              <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-all duration-200">
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-10 w-10 rounded-xl hover:bg-purple-100 hover:text-purple-600 hover:scale-110 transition-all shadow-sm"
                  onClick={() => onEdit(todo)}
                >
                  <Pencil className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-10 w-10 rounded-xl text-red-500 hover:text-red-700 hover:bg-red-100 hover:scale-110 transition-all shadow-sm"
                  onClick={() => setIsDeleteDialogOpen(true)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Description toggle */}
            {todo.description && (
              <Button
                variant="ghost"
                size="sm"
                className="mt-3 -ml-2 h-8 text-xs font-semibold text-gray-600 hover:text-purple-700 hover:bg-purple-100 rounded-xl transition-all"
                onClick={() => setIsExpanded(!isExpanded)}
              >
                {isExpanded ? (
                  <>
                    <ChevronUp className="h-4 w-4 mr-1" />
                    Hide details
                  </>
                ) : (
                  <>
                    <ChevronDown className="h-4 w-4 mr-1" />
                    Show details
                  </>
                )}
              </Button>
            )}

            {/* Expanded description */}
            {isExpanded && todo.description && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-3 rounded-xl bg-gradient-to-r from-purple-50 to-pink-50 p-4 text-sm text-gray-700 border-2 border-purple-200 shadow-sm font-medium"
              >
                {todo.description}
              </motion.div>
            )}
          </div>
        </div>
      </motion.div>

      {/* Delete confirmation dialog */}
      <DeleteConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        onConfirm={handleDelete}
        todoTitle={todo.title}
      />
    </>
  );
}
