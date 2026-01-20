"""Todo API routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.deps.auth import CurrentUser
from src.api.schemas.todo import (
    CompleteResponse,
    CreateTodoRequest,
    TodoListResponse,
    TodoResponse,
    UpdateTodoRequest,
)
from src.core.database import get_session
from src.models.enums import Priority
from src.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get("", response_model=TodoListResponse)
async def list_todos(
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
    completed: bool | None = Query(default=None, description="Filter by completion status"),
    priority: Priority | None = Query(default=None, description="Filter by priority"),
    tag: str | None = Query(default=None, description="Filter by tag name"),
    search: str | None = Query(default=None, description="Search in title and description"),
    sort: str = Query(default="-created_at", description="Sort field (prefix with - for desc)"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
) -> TodoListResponse:
    """List all todos for the current user with optional filters."""
    service = TodoService(session)
    todos, total = await service.list_todos(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        completed=completed,
        priority=priority,
        search=search,
        sort=sort,
    )

    total_pages = (total + page_size - 1) // page_size

    return TodoListResponse(
        items=[TodoResponse.model_validate(todo, from_attributes=True) for todo in todos],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    request: CreateTodoRequest,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TodoResponse:
    """Create a new todo."""
    service = TodoService(session)

    # Strip timezone info from datetime fields (DB uses naive datetime)
    due_date = request.due_date.replace(tzinfo=None) if request.due_date else None
    reminder_time = request.reminder_time.replace(tzinfo=None) if request.reminder_time else None

    todo = await service.create_todo(
        user_id=current_user.id,
        title=request.title,
        description=request.description,
        priority=request.priority,
        due_date=due_date,
        reminder_time=reminder_time,
        recurrence=request.recurrence,
    )
    return TodoResponse.model_validate(todo, from_attributes=True)


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: UUID,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TodoResponse:
    """Get a specific todo by ID."""
    service = TodoService(session)
    todo = await service.get_todo(todo_id=todo_id, user_id=current_user.id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return TodoResponse.model_validate(todo, from_attributes=True)


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: UUID,
    request: UpdateTodoRequest,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TodoResponse:
    """Update an existing todo."""
    service = TodoService(session)
    todo = await service.get_todo(todo_id=todo_id, user_id=current_user.id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    update_data = request.model_dump(exclude_unset=True)
    updated_todo = await service.update_todo(todo, **update_data)

    return TodoResponse.model_validate(updated_todo, from_attributes=True)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: UUID,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    """Delete a todo."""
    service = TodoService(session)
    todo = await service.get_todo(todo_id=todo_id, user_id=current_user.id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    await service.delete_todo(todo)


@router.post("/{todo_id}/complete", response_model=CompleteResponse)
async def complete_todo(
    todo_id: UUID,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CompleteResponse:
    """Mark a todo as complete. For recurring todos, creates the next occurrence."""
    service = TodoService(session)
    todo = await service.get_todo(todo_id=todo_id, user_id=current_user.id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    completed_todo, next_occurrence = await service.complete_todo(todo)

    return CompleteResponse(
        completed_todo=TodoResponse.model_validate(completed_todo, from_attributes=True),
        next_occurrence=TodoResponse.model_validate(next_occurrence, from_attributes=True) if next_occurrence else None,
    )


@router.post("/{todo_id}/incomplete", response_model=TodoResponse)
async def incomplete_todo(
    todo_id: UUID,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TodoResponse:
    """Mark a todo as incomplete."""
    service = TodoService(session)
    todo = await service.get_todo(todo_id=todo_id, user_id=current_user.id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    updated_todo = await service.incomplete_todo(todo)

    return TodoResponse.model_validate(updated_todo, from_attributes=True)
