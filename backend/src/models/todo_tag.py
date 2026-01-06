"""TodoTag junction model for many-to-many relationship."""

from uuid import UUID

from sqlmodel import Field, SQLModel


class TodoTag(SQLModel, table=True):
    """Junction table for Todo-Tag many-to-many relationship."""

    __tablename__ = "todo_tags"

    todo_id: UUID = Field(foreign_key="todos.id", primary_key=True, nullable=False)
    tag_id: UUID = Field(foreign_key="tags.id", primary_key=True, nullable=False)
