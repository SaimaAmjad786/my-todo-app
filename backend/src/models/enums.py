"""Enumeration types for the Todo application."""

from enum import Enum


class Priority(str, Enum):
    """Todo priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Recurrence(str, Enum):
    """Todo recurrence patterns."""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class MessageRole(str, Enum):
    """Chat message roles for AI conversations."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
