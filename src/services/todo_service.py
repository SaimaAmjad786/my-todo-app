"""Todo business logic service with JSON persistence."""

import json
from pathlib import Path
from datetime import datetime, timedelta
from calendar import monthrange
from src.models.todo import Todo


# Available categories
CATEGORIES = ["work", "personal", "shopping", "health", "general"]

# Available recurrence patterns (Advanced Level)
RECURRENCE_PATTERNS = ["none", "daily", "weekly", "monthly"]


def calculate_next_due_date(current_date: str, recurrence: str) -> str:
    """Calculate the next due date based on recurrence pattern.

    Args:
        current_date: Current due date in YYYY-MM-DD format, or empty string.
        recurrence: Recurrence pattern (daily, weekly, monthly).

    Returns:
        Next due date in YYYY-MM-DD format.
    """
    if not current_date:
        # If no current date, use today's date
        base_date = datetime.now()
    else:
        try:
            base_date = datetime.strptime(current_date, "%Y-%m-%d")
        except ValueError:
            base_date = datetime.now()

    if recurrence == "daily":
        next_date = base_date + timedelta(days=1)
    elif recurrence == "weekly":
        next_date = base_date + timedelta(days=7)
    elif recurrence == "monthly":
        # Handle monthly edge cases (29th, 30th, 31st)
        year = base_date.year
        month = base_date.month + 1
        day = base_date.day

        if month > 12:
            month = 1
            year += 1

        # Get max days in target month
        max_day = monthrange(year, month)[1]
        # Use the smaller of original day or max day of month
        target_day = min(day, max_day)

        next_date = datetime(year, month, target_day)
    else:
        # No recurrence or unknown pattern
        return current_date

    return next_date.strftime("%Y-%m-%d")


class TodoService:
    """Manages Todo CRUD operations with JSON file storage."""

    DEFAULT_FILE = "todos.json"

    def __init__(self, file_path: str | None = None) -> None:
        """Initialize the service and load existing data."""
        self._file_path = Path(file_path or self.DEFAULT_FILE)
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1
        self._load()

    def _load(self) -> None:
        """Load todos from JSON file."""
        if self._file_path.exists():
            try:
                with open(self._file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for todo_data in data.get("todos", []):
                        # Handle old todos without category
                        if "category" not in todo_data:
                            todo_data["category"] = "general"
                        # Handle old todos without due_time (Advanced Level)
                        if "due_time" not in todo_data:
                            todo_data["due_time"] = ""
                        # Handle old todos without recurrence (Advanced Level)
                        if "recurrence" not in todo_data:
                            todo_data["recurrence"] = "none"
                        todo = Todo.from_dict(todo_data)
                        self._todos[todo.id] = todo
                    self._next_id = data.get("next_id", 1)
            except (json.JSONDecodeError, KeyError):
                self._todos = {}
                self._next_id = 1

    def _save(self) -> None:
        """Save todos to JSON file."""
        data = {
            "todos": [todo.to_dict() for todo in self._todos.values()],
            "next_id": self._next_id
        }
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_all(self) -> list[Todo]:
        """Return all todos ordered by ID."""
        return sorted(self._todos.values(), key=lambda todo: todo.id)

    def add(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: str = "",
        category: str = "general",
        due_time: str = "",
        recurrence: str = "none"
    ) -> Todo | None:
        """Add a new todo."""
        if not title or not title.strip():
            return None

        if priority not in ("high", "medium", "low"):
            priority = "medium"

        if category not in CATEGORIES:
            category = "general"

        if recurrence not in RECURRENCE_PATTERNS:
            recurrence = "none"

        # Time requires date
        if due_time and not due_date:
            due_time = ""

        todo = Todo(
            id=self._next_id,
            title=title.strip(),
            description=description.strip() if description else "",
            completed=False,
            priority=priority,
            due_date=due_date.strip() if due_date else "",
            category=category,
            due_time=due_time.strip() if due_time else "",
            recurrence=recurrence,
        )
        self._todos[todo.id] = todo
        self._next_id += 1
        self._save()
        return todo

    def get_by_id(self, todo_id: int) -> Todo | None:
        """Get a todo by ID."""
        return self._todos.get(todo_id)

    def update(
        self,
        todo_id: int,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        due_date: str | None = None,
        category: str | None = None,
        due_time: str | None = None,
        recurrence: str | None = None
    ) -> Todo | None:
        """Update a todo's fields."""
        todo = self._todos.get(todo_id)
        if not todo:
            return None

        if title is not None:
            if not title or not title.strip():
                return None
            todo.title = title.strip()

        if description is not None:
            todo.description = description.strip()

        if priority is not None and priority in ("high", "medium", "low"):
            todo.priority = priority

        if due_date is not None:
            todo.due_date = due_date.strip()

        if category is not None and category in CATEGORIES:
            todo.category = category

        if due_time is not None:
            # Time requires date
            if due_time and not todo.due_date:
                pass  # Skip setting time if no date
            else:
                todo.due_time = due_time.strip()

        if recurrence is not None and recurrence in RECURRENCE_PATTERNS:
            todo.recurrence = recurrence

        self._save()
        return todo

    def delete(self, todo_id: int) -> bool:
        """Delete a todo by ID."""
        if todo_id in self._todos:
            del self._todos[todo_id]
            self._reassign_ids()
            self._save()
            return True
        return False

    def _reassign_ids(self) -> None:
        """Reassign IDs starting from 1."""
        todos_list = sorted(self._todos.values(), key=lambda t: t.id)
        self._todos.clear()
        for i, todo in enumerate(todos_list, start=1):
            todo.id = i
            self._todos[todo.id] = todo
        self._next_id = len(self._todos) + 1

    def create_next_occurrence(self, todo: Todo) -> Todo | None:
        """Create the next occurrence of a recurring task.

        Args:
            todo: The completed recurring todo.

        Returns:
            The newly created todo with updated due date, or None if not recurring.
        """
        if todo.recurrence == "none":
            return None

        next_due_date = calculate_next_due_date(todo.due_date, todo.recurrence)

        new_todo = self.add(
            title=todo.title,
            description=todo.description,
            priority=todo.priority,
            due_date=next_due_date,
            category=todo.category,
            due_time=todo.due_time,
            recurrence=todo.recurrence,
        )
        return new_todo

    def set_completed(self, todo_id: int, completed: bool) -> tuple[Todo | None, Todo | None]:
        """Set a todo's completion status.

        If marking a recurring task complete, creates the next occurrence.

        Args:
            todo_id: The ID of the todo to update.
            completed: The new completion status.

        Returns:
            Tuple of (completed_todo, new_recurring_todo_or_none).
        """
        todo = self._todos.get(todo_id)
        if not todo:
            return (None, None)

        todo.completed = completed
        self._save()

        # Create next occurrence if marking a recurring task as complete
        new_todo = None
        if completed and todo.recurrence != "none":
            new_todo = self.create_next_occurrence(todo)

        return (todo, new_todo)

    # ===== NEW FEATURES =====

    def search(self, query: str) -> list[Todo]:
        """Search todos by title or description."""
        query = query.lower().strip()
        if not query:
            return self.get_all()

        results = []
        for todo in self._todos.values():
            if (query in todo.title.lower() or
                query in todo.description.lower()):
                results.append(todo)

        return sorted(results, key=lambda t: t.id)

    def filter_by_status(self, completed: bool | None = None) -> list[Todo]:
        """Filter todos by completion status."""
        todos = self.get_all()

        if completed is None:
            return todos

        return [t for t in todos if t.completed == completed]

    def filter_by_category(self, category: str) -> list[Todo]:
        """Filter todos by category."""
        if category not in CATEGORIES:
            return self.get_all()

        return [t for t in self.get_all() if t.category == category]

    def filter_by_priority(self, priority: str) -> list[Todo]:
        """Filter todos by priority."""
        if priority not in ("high", "medium", "low"):
            return self.get_all()

        return [t for t in self.get_all() if t.priority == priority]

    def sort_by_priority(self, todos: list[Todo] | None = None) -> list[Todo]:
        """Sort todos by priority (high first)."""
        if todos is None:
            todos = self.get_all()

        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(todos, key=lambda t: priority_order.get(t.priority, 1))

    def sort_by_due_date(self, todos: list[Todo] | None = None) -> list[Todo]:
        """Sort todos by due date (earliest first, no date last)."""
        if todos is None:
            todos = self.get_all()

        def date_key(todo: Todo) -> tuple:
            if not todo.due_date:
                return (1, "9999-99-99")  # No date goes last
            return (0, todo.due_date)

        return sorted(todos, key=date_key)

    def get_categories(self) -> list[str]:
        """Get list of available categories."""
        return CATEGORIES.copy()

    def get_stats(self) -> dict:
        """Get statistics about todos."""
        todos = self.get_all()
        total = len(todos)
        completed = sum(1 for t in todos if t.completed)
        pending = total - completed

        by_priority = {
            "high": sum(1 for t in todos if t.priority == "high" and not t.completed),
            "medium": sum(1 for t in todos if t.priority == "medium" and not t.completed),
            "low": sum(1 for t in todos if t.priority == "low" and not t.completed),
        }

        by_category = {}
        for cat in CATEGORIES:
            by_category[cat] = sum(1 for t in todos if t.category == cat)

        overdue = 0
        today = datetime.now().strftime("%Y-%m-%d")
        for t in todos:
            if t.due_date and t.due_date < today and not t.completed:
                overdue += 1

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_priority": by_priority,
            "by_category": by_category,
            "overdue": overdue,
        }

    def get_overdue_todos(self) -> list[Todo]:
        """Get all overdue, incomplete todos.

        Returns:
            List of todos with due date before today that are not completed.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            t for t in self._todos.values()
            if t.due_date and t.due_date < today and not t.completed
        ]

    def get_due_now_todos(self) -> list[Todo]:
        """Get todos due today that are approaching or past their due time.

        Returns:
            List of todos due today with time that is within 1 hour or past.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now()
        results = []

        for t in self._todos.values():
            if t.completed or t.due_date != today:
                continue

            # If no time set, include all todos due today
            if not t.due_time:
                results.append(t)
                continue

            # Parse the due time and check if within 1 hour or past
            try:
                due_hour, due_minute = map(int, t.due_time.split(":"))
                due_datetime = now.replace(hour=due_hour, minute=due_minute, second=0, microsecond=0)
                time_diff = (due_datetime - now).total_seconds() / 60  # minutes

                # Include if past due or within 60 minutes
                if time_diff <= 60:
                    results.append(t)
            except (ValueError, AttributeError):
                # If time parsing fails, include it
                results.append(t)

        return results

    def get_due_today_todos(self) -> list[Todo]:
        """Get all todos due today that are not completed.

        Returns:
            List of incomplete todos with due date equal to today.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            t for t in self._todos.values()
            if t.due_date == today and not t.completed
        ]

    def get_upcoming_todos(self, days: int = 7) -> list[Todo]:
        """Get todos due within the next N days (excluding today and overdue).

        Args:
            days: Number of days to look ahead (default 7).

        Returns:
            List of incomplete todos due between tomorrow and N days from now.
        """
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        future_date = (today + timedelta(days=days)).strftime("%Y-%m-%d")

        return [
            t for t in self._todos.values()
            if t.due_date and today_str < t.due_date <= future_date and not t.completed
        ]

    def filter_by_due_status(self, status: str) -> list[Todo]:
        """Filter todos by due date status.

        Args:
            status: One of 'overdue', 'today', 'upcoming'.

        Returns:
            List of todos matching the due date status.
        """
        if status == "overdue":
            return self.get_overdue_todos()
        elif status == "today":
            return self.get_due_today_todos()
        elif status == "upcoming":
            return self.get_upcoming_todos()
        else:
            return self.get_all()
