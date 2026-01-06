"""User model for authentication."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.todo import Todo
    from src.models.tag import Tag


class User(BaseModel, table=True):
    """User entity for authentication and data ownership."""

    __tablename__ = "users"

    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    name: str | None = Field(default=None, max_length=100)
    hashed_password: str = Field(nullable=False)

    # Relationships
    todos: list["Todo"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")
