"""Todo schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from src.models.enums import Priority, Recurrence


class CreateTodoRequest(BaseModel):
    """Request schema for creating a todo."""

    title: str = Field(min_length=1, max_length=255, description="Todo title")
    description: str | None = Field(default=None, max_length=5000, description="Optional description")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")
    due_date: datetime | None = Field(default=None, description="Optional due date")
    reminder_time: datetime | None = Field(default=None, description="Optional reminder time")
    recurrence: Recurrence = Field(default=Recurrence.NONE, description="Recurrence pattern")
    tag_ids: list[UUID] = Field(default_factory=list, description="List of tag IDs")

    @field_validator("reminder_time")
    @classmethod
    def validate_reminder_time(cls, v: datetime | None, info) -> datetime | None:
        if v and info.data.get("due_date") and v > info.data["due_date"]:
            raise ValueError("Reminder time must be before or on due date")
        return v


class UpdateTodoRequest(BaseModel):
    """Request schema for updating a todo."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    completed: bool | None = Field(default=None)
    priority: Priority | None = Field(default=None)
    due_date: datetime | None = Field(default=None)
    reminder_time: datetime | None = Field(default=None)
    recurrence: Recurrence | None = Field(default=None)
    tag_ids: list[UUID] | None = Field(default=None)


class TagResponse(BaseModel):
    """Response schema for tag data."""

    id: UUID
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TodoResponse(BaseModel):
    """Response schema for todo data."""

    id: UUID
    user_id: UUID
    title: str
    description: str | None
    completed: bool
    priority: Priority
    due_date: datetime | None
    reminder_time: datetime | None
    recurrence: Recurrence
    parent_id: UUID | None
    created_at: datetime
    updated_at: datetime
    tags: list[TagResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class TodoListResponse(BaseModel):
    """Response schema for paginated todo list."""

    items: list[TodoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CompleteResponse(BaseModel):
    """Response schema for completing a recurring todo."""

    completed_todo: TodoResponse
    next_occurrence: TodoResponse | None = None
