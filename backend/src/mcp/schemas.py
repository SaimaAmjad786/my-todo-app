"""MCP tool response schemas for AI chat operations."""

from typing import Any
from uuid import UUID

from pydantic import BaseModel


class ToolResponse(BaseModel):
    """Base response schema for MCP tool operations."""

    success: bool
    message: str
    data: Any | None = None


class TaskCreated(BaseModel):
    """Response when a task is created."""

    task_id: UUID
    title: str
    description: str | None = None


class TaskInfo(BaseModel):
    """Task information for list and get operations."""

    number: int | None = None
    task_id: UUID
    title: str
    description: str | None = None
    completed: bool
    priority: str
    due_date: str | None = None


class TaskList(BaseModel):
    """Response for list_tasks operation."""

    tasks: list[TaskInfo]
    total: int


class ToolError(BaseModel):
    """Error response for tool operations."""

    error_code: str
    message: str
    details: str | None = None
