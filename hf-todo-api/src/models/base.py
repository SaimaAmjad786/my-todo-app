"""Base SQLModel models with UUID primary key and timestamp mixins."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


def utcnow():
    """Return current UTC time as timezone-naive datetime for PostgreSQL."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class UUIDMixin(SQLModel):
    """Mixin providing UUID primary key."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)


class TimestampMixin(SQLModel):
    """Mixin providing created_at and updated_at timestamps."""

    created_at: datetime = Field(
        default_factory=utcnow,
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": utcnow},
    )


class BaseModel(UUIDMixin, TimestampMixin, SQLModel):
    """Base model with UUID primary key and timestamps."""

    pass
