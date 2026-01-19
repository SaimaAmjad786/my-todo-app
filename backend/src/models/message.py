"""Message model for AI chat messages."""

from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship

from src.models.base import BaseModel
from src.models.enums import MessageRole

if TYPE_CHECKING:
    from src.models.conversation import Conversation
    from src.models.user import User


class Message(BaseModel, table=True):
    """Message entity for individual chat messages.

    Each message belongs to a conversation and has a role
    (user, assistant, or system). Tool calls and results
    are stored as JSON for assistant messages.
    """

    __tablename__ = "messages"

    conversation_id: UUID = Field(foreign_key="conversations.id", index=True, nullable=False)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    role: MessageRole = Field(sa_column=Column(String(20), nullable=False))
    content: str = Field(nullable=False)
    tool_calls: Any | None = Field(default=None, sa_column=Column(JSONB))
    tool_results: Any | None = Field(default=None, sa_column=Column(JSONB))

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    user: "User" = Relationship()
