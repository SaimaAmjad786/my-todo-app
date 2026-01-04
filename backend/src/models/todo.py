"""Todo model for task management."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import DateTime, String
from sqlmodel import Field, Relationship

from src.models.base import BaseModel
from src.models.enums import Priority, Recurrence

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.tag import Tag

from src.models.todo_tag import TodoTag


class Todo(BaseModel, table=True):
    """Todo entity for task management."""

    __tablename__ = "todos"

    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    title: str = Field(max_length=255, nullable=False)
    description: str | None = Field(default=None, max_length=5000)
    completed: bool = Field(default=False, nullable=False)
    priority: Priority = Field(
        default=Priority.MEDIUM,
        nullable=False,
        sa_type=String(20),
    )
    due_date: datetime | None = Field(default=None, sa_type=DateTime(timezone=False))
    reminder_time: datetime | None = Field(default=None, sa_type=DateTime(timezone=False))
    recurrence: Recurrence = Field(
        default=Recurrence.NONE,
        nullable=False,
        sa_type=String(20),
    )
    parent_id: UUID | None = Field(default=None, foreign_key="todos.id")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="todos")
    tags: list["Tag"] = Relationship(back_populates="todos", link_model=TodoTag)
    parent: Optional["Todo"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Todo.id"},
    )
    children: list["Todo"] = Relationship(back_populates="parent")
