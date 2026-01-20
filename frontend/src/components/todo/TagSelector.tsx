"use client";

import { useState } from "react";
import type { Tag } from "@/types/api";
import { useCreateTag } from "@/hooks/useTags";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { X, Plus, Tag as TagIcon, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface TagSelectorProps {
  selectedIds: string[];
  onChange: (ids: string[]) => void;
  availableTags: Tag[];
}

const suggestedTags = ["Work", "Shopping", "Personal", "Health"];

export function TagSelector({ selectedIds, onChange, availableTags }: TagSelectorProps) {
  const [newTagName, setNewTagName] = useState("");
  const createTag = useCreateTag();

  const selectedTags = availableTags.filter((tag) => selectedIds.includes(tag.id));
  const unselectedTags = availableTags.filter((tag) => !selectedIds.includes(tag.id));

  const handleAddTag = (tagId: string) => {
    onChange([...selectedIds, tagId]);
  };

  const handleRemoveTag = (tagId: string) => {
    onChange(selectedIds.filter((id) => id !== tagId));
  };

  const handleCreateTag = async (name?: string) => {
    const tagName = name || newTagName.trim();
    if (!tagName) return;
    try {
      const newTag = await createTag.mutateAsync({ name: tagName });
      onChange([...selectedIds, newTag.id]);
      setNewTagName("");
    } catch {
      // Error handled by mutation
    }
  };

  // Filter suggested tags that don't exist yet
  const availableSuggestions = suggestedTags.filter(
    (suggestion) => !availableTags.some((tag) => tag.name.toLowerCase() === suggestion.toLowerCase())
  );

  return (
    <div className="space-y-4">
      {/* Selected tags */}
      {selectedTags.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-wrap gap-2"
        >
          {selectedTags.map((tag) => (
            <motion.div
              key={tag.id}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
            >
              <Badge
                variant="secondary"
                className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 border-0 shadow-sm hover:shadow-md transition-all"
              >
                <TagIcon className="h-3 w-3" />
                {tag.name}
                <button
                  type="button"
                  onClick={() => handleRemoveTag(tag.id)}
                  className="ml-1 hover:text-pink-600 transition-colors"
                >
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Available tags to add */}
      {unselectedTags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {unselectedTags.map((tag) => (
            <motion.button
              key={tag.id}
              type="button"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleAddTag(tag.id)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium text-gray-600 bg-gray-50 border border-gray-200 hover:bg-purple-50 hover:border-purple-200 hover:text-purple-600 transition-all duration-200"
            >
              <Plus className="h-3 w-3" />
              {tag.name}
            </motion.button>
          ))}
        </div>
      )}

      {/* Suggested tags */}
      {availableSuggestions.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs text-gray-400 flex items-center gap-1">
            <Sparkles className="h-3 w-3" />
            Quick add:
          </p>
          <div className="flex flex-wrap gap-2">
            {availableSuggestions.map((suggestion) => (
              <motion.button
                key={suggestion}
                type="button"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleCreateTag(suggestion)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium text-purple-600 bg-purple-50 border border-purple-200 border-dashed hover:bg-purple-100 hover:border-purple-300 transition-all duration-200"
              >
                <Plus className="h-3 w-3" />
                {suggestion}
              </motion.button>
            ))}
          </div>
        </div>
      )}

      {/* Create new tag */}
      <div className="flex gap-2">
        <div className="relative flex-1 group">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-pink-400 rounded-xl opacity-0 group-focus-within:opacity-100 blur transition-opacity -z-10 scale-[1.02]" />
          <Input
            placeholder="Create new tag..."
            value={newTagName}
            onChange={(e) => setNewTagName(e.target.value)}
            className="h-10 pl-10 text-sm rounded-xl transition-all duration-200 border-gray-200 bg-gray-50/80 focus:bg-white focus:border-purple-400 focus:ring-2 focus:ring-purple-100"
            onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), handleCreateTag())}
          />
          <TagIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 group-focus-within:text-purple-500 transition-colors" />
        </div>
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => handleCreateTag()}
          disabled={!newTagName.trim() || createTag.isPending}
          className="h-10 px-4 rounded-xl border-purple-200 hover:bg-purple-50 hover:border-purple-300 hover:text-purple-600 transition-all duration-200"
        >
          {createTag.isPending ? (
            <div className="w-4 h-4 border-2 border-purple-300 border-t-purple-600 rounded-full animate-spin" />
          ) : (
            "Add"
          )}
        </Button>
      </div>
    </div>
  );
}
