"""Tag model for organizing todos."""

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.todo import Todo

from src.models.todo_tag import TodoTag


class Tag(BaseModel, table=True):
    """Tag entity for categorizing todos."""

    __tablename__ = "tags"

    name: str = Field(max_length=50, nullable=False)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tags")
    todos: list["Todo"] = Relationship(
        back_populates="tags",
        link_model=TodoTag,
    )
