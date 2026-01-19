"""MCP tools for todo operations.

All tools operate on the authenticated user's todos only.
The agent must never modify the database directly - all operations
go through these tools which use the TodoService.
"""

from uuid import UUID
from typing import Any
from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.enums import Priority
from src.services.todo_service import TodoService
from src.mcp.schemas import ToolResponse, TaskCreated, TaskInfo, TaskList


async def add_task(
    session: AsyncSession,
    user_id: UUID,
    title: str,
    description: str | None = None,
    priority: str = "medium",
    due_date: str | None = None,
) -> dict[str, Any]:
    """Create a new todo task for the user."""
    try:
        service = TodoService(session)
        priority_enum = Priority(priority.lower()) if priority else Priority.MEDIUM

        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except ValueError:
                return ToolResponse(
                    success=False,
                    message=f"Invalid due_date format: {due_date}. Use ISO format.",
                ).model_dump(mode="json")

        todo = await service.create_todo(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority_enum,
            due_date=parsed_due_date,
        )

        return ToolResponse(
            success=True,
            message=f"Task '{title}' created successfully.",
            data=TaskCreated(
                task_id=todo.id,
                title=todo.title,
                description=todo.description,
            ).model_dump(mode="json"),
        ).model_dump(mode="json")

    except Exception as e:
        return ToolResponse(success=False, message=f"Failed to create task: {str(e)}").model_dump(mode="json")


async def list_tasks(
    session: AsyncSession,
    user_id: UUID,
    status: str | None = None,
    priority: str | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    """List todos for the user with optional filters."""
    try:
        service = TodoService(session)

        completed = None
        if status == "completed":
            completed = True
        elif status == "pending":
            completed = False

        priority_enum = None
        if priority:
            try:
                priority_enum = Priority(priority.lower())
            except ValueError:
                pass

        todos, total = await service.list_todos(
            user_id=user_id,
            completed=completed,
            priority=priority_enum,
            search=search,
            page_size=100,
        )

        task_list = [
            TaskInfo(
                number=idx + 1,
                task_id=todo.id,
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
                priority=todo.priority.value if hasattr(todo.priority, 'value') else str(todo.priority),
                due_date=todo.due_date.isoformat() if todo.due_date else None,
            )
            for idx, todo in enumerate(todos)
        ]

        # Create formatted display string for AI to use
        formatted_tasks = []
        for idx, todo in enumerate(todos):
            status = "✅" if todo.completed else "⬜"
            priority = todo.priority.value if hasattr(todo.priority, 'value') else str(todo.priority)
            desc = f" - {todo.description}" if todo.description else ""
            due = f" | Due: {todo.due_date.strftime('%Y-%m-%d')}" if todo.due_date else ""
            formatted_tasks.append(f"{idx + 1}. {status} {todo.title}{desc} | Priority: {priority}{due}")

        display_text = "\n".join(formatted_tasks) if formatted_tasks else "No tasks found."

        return ToolResponse(
            success=True,
            message=f"Found {total} task(s). Display this exactly:\n{display_text}",
            data=TaskList(tasks=task_list, total=total).model_dump(mode="json"),
        ).model_dump(mode="json")

    except Exception as e:
        return ToolResponse(success=False, message=f"Failed to list tasks: {str(e)}").model_dump(mode="json")


async def complete_task(
    session: AsyncSession,
    user_id: UUID,
    task_id: str,
) -> dict[str, Any]:
    """Mark a task as completed."""
    try:
        service = TodoService(session)

        try:
            task_uuid = UUID(task_id)
        except ValueError:
            return ToolResponse(success=False, message=f"Invalid task ID: {task_id}").model_dump(mode="json")

        todo = await service.get_todo(task_uuid, user_id)
        if not todo:
            return ToolResponse(success=False, message=f"Task not found: {task_id}").model_dump(mode="json")

        if todo.completed:
            return ToolResponse(success=True, message=f"Task '{todo.title}' is already completed.").model_dump(mode="json")

        completed_todo, next_todo = await service.complete_todo(todo)
        message = f"Task '{completed_todo.title}' marked as completed."
        if next_todo:
            message += f" Next occurrence created."

        return ToolResponse(
            success=True,
            message=message,
            data=TaskInfo(
                task_id=completed_todo.id,
                title=completed_todo.title,
                description=completed_todo.description,
                completed=completed_todo.completed,
                priority=completed_todo.priority.value if hasattr(completed_todo.priority, 'value') else str(completed_todo.priority),
                due_date=completed_todo.due_date.isoformat() if completed_todo.due_date else None,
            ).model_dump(mode="json"),
        ).model_dump(mode="json")

    except Exception as e:
        return ToolResponse(success=False, message=f"Failed to complete task: {str(e)}").model_dump(mode="json")


async def update_task(
    session: AsyncSession,
    user_id: UUID,
    task_id: str,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    due_date: str | None = None,
) -> dict[str, Any]:
    """Update a task's fields."""
    try:
        service = TodoService(session)

        try:
            task_uuid = UUID(task_id)
        except ValueError:
            return ToolResponse(success=False, message=f"Invalid task ID: {task_id}").model_dump(mode="json")

        todo = await service.get_todo(task_uuid, user_id)
        if not todo:
            return ToolResponse(success=False, message=f"Task not found: {task_id}").model_dump(mode="json")

        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if priority is not None:
            try:
                update_data["priority"] = Priority(priority.lower())
            except ValueError:
                return ToolResponse(success=False, message=f"Invalid priority: {priority}").model_dump(mode="json")
        if due_date is not None:
            try:
                update_data["due_date"] = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except ValueError:
                return ToolResponse(success=False, message=f"Invalid due_date: {due_date}").model_dump(mode="json")

        if not update_data:
            return ToolResponse(success=False, message="No fields to update.").model_dump(mode="json")

        updated_todo = await service.update_todo(todo, **update_data)

        return ToolResponse(
            success=True,
            message=f"Task '{updated_todo.title}' updated.",
            data=TaskInfo(
                task_id=updated_todo.id,
                title=updated_todo.title,
                description=updated_todo.description,
                completed=updated_todo.completed,
                priority=updated_todo.priority.value if hasattr(updated_todo.priority, 'value') else str(updated_todo.priority),
                due_date=updated_todo.due_date.isoformat() if updated_todo.due_date else None,
            ).model_dump(mode="json"),
        ).model_dump(mode="json")

    except Exception as e:
        return ToolResponse(success=False, message=f"Failed to update task: {str(e)}").model_dump(mode="json")


async def delete_task(
    session: AsyncSession,
    user_id: UUID,
    task_id: str,
) -> dict[str, Any]:
    """Delete a task permanently."""
    try:
        service = TodoService(session)

        try:
            task_uuid = UUID(task_id)
        except ValueError:
            return ToolResponse(success=False, message=f"Invalid task ID: {task_id}").model_dump(mode="json")

        todo = await service.get_todo(task_uuid, user_id)
        if not todo:
            return ToolResponse(success=False, message=f"Task not found: {task_id}").model_dump(mode="json")

        task_title = todo.title
        await service.delete_todo(todo)

        return ToolResponse(success=True, message=f"Task '{task_title}' deleted.").model_dump(mode="json")

    except Exception as e:
        return ToolResponse(success=False, message=f"Failed to delete task: {str(e)}").model_dump(mode="json")


# Tool definitions for OpenAI function calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new todo task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title (required)"},
                    "description": {"type": "string", "description": "Task description"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                    "due_date": {"type": "string", "description": "Due date in ISO format"},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks with optional filters",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["all", "completed", "pending"]},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                    "search": {"type": "string", "description": "Search term"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Task UUID"},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update task title, description, priority, or due date",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Task UUID"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                    "due_date": {"type": "string"},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task permanently. Cannot be undone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Task UUID"},
                },
                "required": ["task_id"],
            },
        },
    },
]
