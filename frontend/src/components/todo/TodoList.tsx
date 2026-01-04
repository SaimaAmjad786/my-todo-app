"use client";

import { useState } from "react";
import type { Todo, TodoFilters } from "@/types/api";
import { useTodos, useDeleteTodo, useCompleteTodo, useIncompleteTodo } from "@/hooks/useTodos";
import { useReminders } from "@/hooks/useReminders";
import { TodoItem } from "./TodoItem";
import { TodoForm } from "./TodoForm";
import { EmptyState } from "./EmptyState";
import { TodoListSkeleton } from "./TodoListSkeleton";
import { SearchInput } from "./SearchInput";
import { FilterBar } from "./FilterBar";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Plus } from "lucide-react";

export function TodoList() {
  const [filters, setFilters] = useState<TodoFilters>({
    sort: "-created_at",
    page: 1,
    page_size: 20,
  });
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);

  const { data, isLoading, isError, error } = useTodos(filters);
  const deleteTodo = useDeleteTodo();
  const completeTodo = useCompleteTodo();
  const incompleteTodo = useIncompleteTodo();

  // Set up reminder notifications for todos
  useReminders(data?.items);

  const handleSearch = (search: string) => {
    setFilters((prev) => ({ ...prev, search: search || undefined, page: 1 }));
  };

  const handleFilterChange = (newFilters: Partial<TodoFilters>) => {
    setFilters((prev) => ({ ...prev, ...newFilters, page: 1 }));
  };

  const handleToggleComplete = (todo: Todo) => {
    if (todo.completed) {
      incompleteTodo.mutate(todo.id);
    } else {
      completeTodo.mutate(todo.id);
    }
  };

  const handleDelete = (todoId: string) => {
    deleteTodo.mutate(todoId);
  };

  const handleEdit = (todo: Todo) => {
    setEditingTodo(todo);
  };

  const handleCreateSuccess = () => {
    setIsCreateDialogOpen(false);
  };

  const handleEditSuccess = () => {
    setEditingTodo(null);
  };

  if (isError) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-600">
        <p className="font-medium">Error loading todos</p>
        <p className="text-sm">{error instanceof Error ? error.message : "Unknown error"}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with search and create button */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <SearchInput onSearch={handleSearch} initialValue={filters.search} />
        <Button
          onClick={() => setIsCreateDialogOpen(true)}
          className="flex items-center gap-2 h-12 px-6 text-base font-bold bg-gradient-to-r from-purple-600 via-pink-500 to-purple-600 hover:from-purple-700 hover:via-pink-600 hover:to-purple-700 rounded-2xl shadow-lg shadow-purple-300/50 hover:shadow-xl hover:shadow-pink-300/50 hover:scale-105 active:scale-95 transition-all duration-300"
        >
          <Plus className="h-5 w-5" />
          New Todo
        </Button>
      </div>

      {/* Filters */}
      <FilterBar filters={filters} onFilterChange={handleFilterChange} />

      {/* Todo list */}
      {isLoading ? (
        <TodoListSkeleton />
      ) : !data?.items?.length ? (
        <EmptyState onCreateClick={() => setIsCreateDialogOpen(true)} />
      ) : (
        <div className="space-y-3">
          {data.items.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
              onEdit={handleEdit}
            />
          ))}

          {/* Pagination info */}
          {data.total_pages > 1 && (
            <div className="flex items-center justify-between pt-4 text-sm text-gray-500">
              <span>
                Page {data.page} of {data.total_pages} ({data.total} todos)
              </span>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={data.page <= 1}
                  onClick={() => setFilters((prev) => ({ ...prev, page: (prev.page || 1) - 1 }))}
                >
                  Previous
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={data.page >= data.total_pages}
                  onClick={() => setFilters((prev) => ({ ...prev, page: (prev.page || 1) + 1 }))}
                >
                  Next
                </Button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Create Todo Dialog */}
      <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
        <DialogContent className="sm:max-w-[340px] p-0 gap-0 rounded-3xl border-0 shadow-2xl shadow-purple-300/30 overflow-hidden">
          <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-3">
            <DialogHeader>
              <DialogTitle className="text-white text-base font-semibold flex items-center gap-2">
                <Plus className="w-4 h-4" />
                Create New Todo
              </DialogTitle>
            </DialogHeader>
          </div>
          <div className="p-4">
            <TodoForm onSuccess={handleCreateSuccess} onCancel={() => setIsCreateDialogOpen(false)} />
          </div>
        </DialogContent>
      </Dialog>

      {/* Edit Todo Dialog */}
      <Dialog open={!!editingTodo} onOpenChange={() => setEditingTodo(null)}>
        <DialogContent className="sm:max-w-[380px] p-0 gap-0 rounded-3xl border-0 shadow-2xl shadow-purple-300/30 overflow-hidden">
          <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-4">
            <DialogHeader>
              <DialogTitle className="text-white text-lg font-semibold">Edit Todo</DialogTitle>
            </DialogHeader>
          </div>
          <div className="p-5">
            {editingTodo && (
              <TodoForm
                todo={editingTodo}
                onSuccess={handleEditSuccess}
                onCancel={() => setEditingTodo(null)}
              />
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
