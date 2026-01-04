"""Todo service for business logic and data access."""

from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.todo import Todo
from src.models.enums import Priority, Recurrence
from src.services.recurrence import calculate_next_due_date, calculate_next_reminder_time


class TodoService:
    """Service for todo CRUD operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_todos(
        self,
        user_id: UUID,
        *,
        page: int = 1,
        page_size: int = 20,
        completed: bool | None = None,
        priority: Priority | None = None,
        search: str | None = None,
        tag_id: UUID | None = None,
        sort: str = "-created_at",
    ) -> tuple[list[Todo], int]:
        """List todos for a user with optional filters.

        Args:
            user_id: Owner's user ID
            page: Page number (1-indexed)
            page_size: Items per page
            completed: Filter by completion status
            priority: Filter by priority
            search: Search term for title/description
            tag_id: Filter by tag
            sort: Sort field (prefix with - for descending)

        Returns:
            Tuple of (todos list, total count)
        """
        query = select(Todo).where(Todo.user_id == user_id).options(selectinload(Todo.tags))

        # Apply filters
        if completed is not None:
            query = query.where(Todo.completed == completed)
        if priority is not None:
            query = query.where(Todo.priority == priority)
        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                (Todo.title.ilike(search_pattern)) | (Todo.description.ilike(search_pattern))
            )

        # Count total before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()

        # Apply sorting
        descending = sort.startswith("-")
        sort_field = sort[1:] if descending else sort
        sort_column = getattr(Todo, sort_field, Todo.created_at)
        if descending:
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column)

        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self.session.execute(query)
        todos = list(result.scalars().all())

        return todos, total

    async def get_todo(self, todo_id: UUID, user_id: UUID) -> Todo | None:
        """Get a todo by ID for a specific user.

        Args:
            todo_id: Todo ID
            user_id: Owner's user ID

        Returns:
            Todo if found and owned by user, None otherwise
        """
        result = await self.session.execute(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id).options(selectinload(Todo.tags))
        )
        return result.scalar_one_or_none()

    async def create_todo(self, user_id: UUID, **data) -> Todo:
        """Create a new todo.

        Args:
            user_id: Owner's user ID
            **data: Todo fields

        Returns:
            Created todo
        """
        todo = Todo(user_id=user_id, **data)
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        # Reload with tags relationship
        return await self.get_todo(todo.id, user_id)

    async def update_todo(self, todo: Todo, **data) -> Todo:
        """Update a todo.

        Args:
            todo: Todo to update
            **data: Fields to update

        Returns:
            Updated todo
        """
        for key, value in data.items():
            if value is not None:
                setattr(todo, key, value)
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        # Reload with tags relationship
        return await self.get_todo(todo.id, todo.user_id)

    async def delete_todo(self, todo: Todo) -> None:
        """Delete a todo.

        Args:
            todo: Todo to delete
        """
        await self.session.delete(todo)
        await self.session.commit()

    async def complete_todo(self, todo: Todo) -> tuple[Todo, Todo | None]:
        """Mark a todo as complete, creating next occurrence if recurring.

        Args:
            todo: Todo to complete

        Returns:
            Tuple of (completed todo, next occurrence or None)
        """
        todo.completed = True
        self.session.add(todo)

        next_todo = None
        if todo.recurrence != Recurrence.NONE and todo.due_date:
            # Calculate next due date
            next_due_date = calculate_next_due_date(todo.recurrence, todo.due_date)
            
            # Calculate next reminder if exists
            next_reminder = None
            if todo.reminder_time:
                next_reminder = calculate_next_reminder_time(
                    todo.recurrence, todo.due_date, todo.reminder_time, next_due_date
                )
            
            # Create next occurrence
            next_todo = Todo(
                user_id=todo.user_id,
                title=todo.title,
                description=todo.description,
                completed=False,
                priority=todo.priority,
                due_date=next_due_date,
                reminder_time=next_reminder,
                recurrence=todo.recurrence,
                parent_id=todo.id,
            )
            self.session.add(next_todo)

        await self.session.commit()
        # Reload with tags relationship
        completed = await self.get_todo(todo.id, todo.user_id)
        next_occurrence = None
        if next_todo:
            next_occurrence = await self.get_todo(next_todo.id, next_todo.user_id)

        return completed, next_occurrence

    async def incomplete_todo(self, todo: Todo) -> Todo:
        """Mark a todo as incomplete.

        Args:
            todo: Todo to mark incomplete

        Returns:
            Updated todo
        """
        todo.completed = False
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        # Reload with tags relationship
        return await self.get_todo(todo.id, todo.user_id)
