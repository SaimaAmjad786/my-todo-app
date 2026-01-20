/**
 * API client utility with fetch wrapper and error handling.
 */

import { ErrorResponse } from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getAuthHeaders(): HeadersInit {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  return headers;
}

// Custom JSON stringify that converts timezone-aware datetimes to naive (ISO format without timezone)
function stringifyWithNaiveDates(obj: unknown): string {
  return JSON.stringify(obj, (_key, value) => {
    if (value instanceof Date) {
      // Convert to naive datetime (without timezone) for PostgreSQL compatibility
      // This strips the timezone info by treating the date as if it's in local time
      const naiveDate = new Date(value.getTime() + value.getTimezoneOffset() * 60000);
      return naiveDate.toISOString().slice(0, 19); // Return "YYYY-MM-DDTHH:mm:ss" format
    }
    return value;
  });
}

export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
    public details?: Array<{ field: string; message: string }>
  ) {
    super(message);
    this.name = "ApiError";
  }
}

interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean | undefined>;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorData: ErrorResponse | null = null;
    try {
      errorData = await response.json();
    } catch {
      // Response body might not be JSON
    }

    throw new ApiError(
      response.status,
      errorData?.error?.code || "UNKNOWN_ERROR",
      errorData?.error?.message || response.statusText || `HTTP error ${response.status}`,
      errorData?.error?.details
    );
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

function buildUrl(endpoint: string, params?: Record<string, string | number | boolean | undefined>): string {
  const url = new URL(`${API_BASE_URL}${endpoint}`);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        url.searchParams.append(key, String(value));
      }
    });
  }

  return url.toString();
}

export async function apiGet<T>(endpoint: string, options?: RequestOptions): Promise<T> {
  const { params, ...fetchOptions } = options || {};
  const url = buildUrl(endpoint, params);

  const response = await fetch(url, {
    method: "GET",
    headers: {
      ...getAuthHeaders(),
      ...fetchOptions?.headers,
    },
    ...fetchOptions,
  });

  return handleResponse<T>(response);
}

export async function apiPost<T, D = unknown>(
  endpoint: string,
  data?: D,
  options?: RequestOptions
): Promise<T> {
  const { params, ...fetchOptions } = options || {};
  const url = buildUrl(endpoint, params);

  const response = await fetch(url, {
    method: "POST",
    headers: {
      ...getAuthHeaders(),
      ...fetchOptions?.headers,
    },
    body: data ? stringifyWithNaiveDates(data) : undefined,
    ...fetchOptions,
  });

  return handleResponse<T>(response);
}

export async function apiPatch<T, D = unknown>(
  endpoint: string,
  data: D,
  options?: RequestOptions
): Promise<T> {
  const { params, ...fetchOptions } = options || {};
  const url = buildUrl(endpoint, params);

  const response = await fetch(url, {
    method: "PATCH",
    headers: {
      ...getAuthHeaders(),
      ...fetchOptions?.headers,
    },
    body: stringifyWithNaiveDates(data),
    ...fetchOptions,
  });

  return handleResponse<T>(response);
}

export async function apiDelete<T = void>(
  endpoint: string,
  options?: RequestOptions
): Promise<T> {
  const { params, ...fetchOptions } = options || {};
  const url = buildUrl(endpoint, params);

  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      ...getAuthHeaders(),
      ...fetchOptions?.headers,
    },
    ...fetchOptions,
  });

  return handleResponse<T>(response);
}
