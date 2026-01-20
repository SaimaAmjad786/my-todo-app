"""Tag schemas for request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateTagRequest(BaseModel):
    """Request schema for creating a tag."""

    name: str = Field(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9 -]+$")


class TagResponse(BaseModel):
    """Response schema for tag data."""

    id: UUID
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}
