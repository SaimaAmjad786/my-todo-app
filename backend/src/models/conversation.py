"""Conversation model for AI chat sessions."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.message import Message


class Conversation(BaseModel, table=True):
    """Conversation entity for AI chat sessions.

    Each conversation belongs to a single user and contains
    multiple messages. Conversations are persisted in the database
    to enable resumption after server restarts.
    """

    __tablename__ = "conversations"

    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    title: str | None = Field(default=None, max_length=100)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "order_by": "Message.created_at"},
    )
