"""Recurrence calculation utility for recurring todos."""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from src.models.enums import Recurrence


def calculate_next_due_date(recurrence: Recurrence, current_due_date: datetime) -> datetime:
    """Calculate the next due date based on recurrence pattern.

    Args:
        recurrence: The recurrence pattern
        current_due_date: The current due date

    Returns:
        The next due date based on the recurrence pattern
    """
    if recurrence == Recurrence.DAILY:
        return current_due_date + timedelta(days=1)
    elif recurrence == Recurrence.WEEKLY:
        return current_due_date + timedelta(weeks=1)
    elif recurrence == Recurrence.MONTHLY:
        return current_due_date + relativedelta(months=1)
    else:
        return current_due_date


def calculate_next_reminder_time(
    recurrence: Recurrence,
    current_due_date: datetime,
    current_reminder_time: datetime,
    next_due_date: datetime,
) -> datetime:
    """Calculate the next reminder time based on the offset from due date.

    Args:
        recurrence: The recurrence pattern
        current_due_date: The current due date
        current_reminder_time: The current reminder time
        next_due_date: The next due date

    Returns:
        The next reminder time maintaining the same offset from due date
    """
    offset = current_due_date - current_reminder_time
    return next_due_date - offset
