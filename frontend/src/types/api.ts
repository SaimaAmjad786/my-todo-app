/**
 * TypeScript type definitions matching OpenAPI schemas.
 */

// Enums
export type Priority = "high" | "medium" | "low";
export type Recurrence = "none" | "daily" | "weekly" | "monthly";

// User types
export interface User {
  id: string;
  email: string;
  name: string | null;
  created_at: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  name?: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
}

// Todo types
export interface Tag {
  id: string;
  name: string;
  created_at: string;
}

export interface Todo {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: Priority;
  due_date: string | null;
  reminder_time: string | null;
  recurrence: Recurrence;
  parent_id: string | null;
  tags: Tag[];
  created_at: string;
  updated_at: string;
}

export interface CreateTodoRequest {
  title: string;
  description?: string;
  priority?: Priority;
  due_date?: string;
  reminder_time?: string;
  recurrence?: Recurrence;
  tag_ids?: string[];
}

export interface UpdateTodoRequest {
  title?: string;
  description?: string | null;
  completed?: boolean;
  priority?: Priority;
  due_date?: string | null;
  reminder_time?: string | null;
  recurrence?: Recurrence;
  tag_ids?: string[];
}

export interface TodoListResponse {
  items: Todo[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface CompleteTodoResponse {
  completed_todo: Todo;
  next_occurrence: Todo | null;
}

// Tag types
export interface CreateTagRequest {
  name: string;
}

// Error types
export interface ErrorDetail {
  field: string;
  message: string;
}

export interface ErrorBody {
  code: string;
  message: string;
  details?: ErrorDetail[];
}

export interface ErrorResponse {
  error: ErrorBody;
}

// Filter types for list todos
export interface TodoFilters {
  completed?: boolean;
  priority?: Priority;
  tag?: string;
  search?: string;
  sort?: string;
  page?: number;
  page_size?: number;
}

// Chat types
export interface ToolCall {
  tool: string;
  arguments: Record<string, unknown>;
  result: Record<string, unknown>;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
}

export interface ConversationInfo {
  id: string;
  title: string | null;
  created_at: string;
  updated_at: string;
}

export interface ConversationListResponse {
  conversations: ConversationInfo[];
  total: number;
}

export interface MessageInfo {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  tool_calls?: ToolCall[];
  created_at: string;
}

export interface ConversationDetailResponse {
  conversation: ConversationInfo;
  messages: MessageInfo[];
}
