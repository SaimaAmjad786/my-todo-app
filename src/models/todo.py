"""Todo domain model."""

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Todo:
    """Represents a task item.

    Attributes:
        id: Unique integer identifier, auto-generated.
        title: Non-empty string describing the task.
        description: Optional additional detail about the task.
        completed: Whether the task is done.
        priority: Priority level (high, medium, low).
        due_date: Optional due date string (YYYY-MM-DD).
        category: Category tag (work, personal, shopping, health, general).
        due_time: Optional due time string (HH:MM, 24-hour format).
        recurrence: Recurrence pattern (none, daily, weekly, monthly).
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "medium"
    due_date: str = ""
    category: str = "general"
    due_time: str = ""
    recurrence: str = "none"

    def to_dict(self) -> dict[str, Any]:
        """Convert todo to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Todo":
        """Create todo from dictionary."""
        return cls(**data)
