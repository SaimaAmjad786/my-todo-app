"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiDelete, apiGet, apiPost } from "@/lib/api-client";
import type { Tag, CreateTagRequest } from "@/types/api";

const TAGS_QUERY_KEY = "tags";

export function useTags() {
  return useQuery({
    queryKey: [TAGS_QUERY_KEY],
    queryFn: () => apiGet<Tag[]>("/tags"),
  });
}

export function useCreateTag() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateTagRequest) => apiPost<Tag>("/tags", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TAGS_QUERY_KEY] });
    },
  });
}

export function useDeleteTag() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (tagId: string) => apiDelete(`/tags/${tagId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TAGS_QUERY_KEY] });
    },
  });
}
