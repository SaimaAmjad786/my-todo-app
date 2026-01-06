"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiDelete, apiGet, apiPatch, apiPost } from "@/lib/api-client";
import type {
  Todo,
  TodoListResponse,
  CreateTodoRequest,
  UpdateTodoRequest,
  CompleteTodoResponse,
  TodoFilters,
} from "@/types/api";

const TODOS_QUERY_KEY = "todos";

export function useTodos(filters: TodoFilters = {}) {
  return useQuery({
    queryKey: [TODOS_QUERY_KEY, filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.completed !== undefined) params.set("completed", String(filters.completed));
      if (filters.priority) params.set("priority", filters.priority);
      if (filters.tag) params.set("tag", filters.tag);
      if (filters.search) params.set("search", filters.search);
      if (filters.sort) params.set("sort", filters.sort);
      if (filters.page) params.set("page", String(filters.page));
      if (filters.page_size) params.set("page_size", String(filters.page_size));

      const queryString = params.toString();
      const url = queryString ? `/todos?${queryString}` : "/todos";
      return apiGet<TodoListResponse>(url);
    },
  });
}

export function useTodo(todoId: string | null) {
  return useQuery({
    queryKey: [TODOS_QUERY_KEY, todoId],
    queryFn: async () => {
      if (!todoId) return null;
      return apiGet<Todo>(`/todos/${todoId}`);
    },
    enabled: !!todoId,
  });
}

export function useCreateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateTodoRequest) => apiPost<Todo>("/todos", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TODOS_QUERY_KEY] });
    },
  });
}

export function useUpdateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ todoId, data }: { todoId: string; data: UpdateTodoRequest }) =>
      apiPatch<Todo>(`/todos/${todoId}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TODOS_QUERY_KEY] });
    },
  });
}

export function useDeleteTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (todoId: string) => apiDelete(`/todos/${todoId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TODOS_QUERY_KEY] });
    },
  });
}

export function useCompleteTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (todoId: string) =>
      apiPost<CompleteTodoResponse>(`/todos/${todoId}/complete`, {}),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TODOS_QUERY_KEY] });
    },
  });
}

export function useIncompleteTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (todoId: string) =>
      apiPost<Todo>(`/todos/${todoId}/incomplete`, {}),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TODOS_QUERY_KEY] });
    },
  });
}
