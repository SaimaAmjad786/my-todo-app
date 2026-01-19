"""Chat schemas for request/response validation."""

from datetime import datetime
from uuid import UUID
from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """Schema for tool call information."""

    tool: str = Field(description="Tool name")
    arguments: dict[str, Any] = Field(description="Tool arguments")
    result: dict[str, Any] = Field(description="Tool result")


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    message: str = Field(min_length=1, max_length=10000, description="User message")
    conversation_id: UUID | None = Field(default=None, description="Existing conversation ID to continue")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    conversation_id: UUID = Field(description="Conversation ID")
    response: str = Field(description="Assistant response text")
    tool_calls: list[ToolCall] = Field(default_factory=list, description="Tools called during processing")


class ConversationInfo(BaseModel):
    """Schema for conversation metadata."""

    id: UUID
    title: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversationListResponse(BaseModel):
    """Response schema for listing conversations."""

    conversations: list[ConversationInfo]
    total: int


class MessageInfo(BaseModel):
    """Schema for message data."""

    id: UUID
    role: str
    content: str
    tool_calls: list[ToolCall] | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationDetailResponse(BaseModel):
    """Response schema for conversation with messages."""

    conversation: ConversationInfo
    messages: list[MessageInfo]
