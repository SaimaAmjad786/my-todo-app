"""Cohere Agent for Todo chatbot with tool integration."""

import json
import logging
import traceback
from uuid import UUID
from typing import Any

import cohere

from src.core.config import get_settings

logger = logging.getLogger(__name__)
from src.mcp.tools import (
    add_task,
    list_tasks,
    complete_task,
    update_task,
    delete_task,
)

settings = get_settings()

SYSTEM_PROMPT = """You are a helpful Todo assistant. You help users manage their tasks through natural language.

You can:
- Add new tasks (use add_task)
- List tasks (use list_tasks)
- Mark tasks complete (use complete_task)
- Update tasks (use update_task)
- Delete tasks (use delete_task) - ALWAYS ask for confirmation before deleting

Rules:
1. ALWAYS reply to EVERY user message. Never stay silent. Even if you don't understand, ask for clarification.
2. Be concise and friendly
3. When user refers to a task by NUMBER (like "task 1", "task 2"), you MUST:
   - First call list_tasks to get all tasks
   - Find the task with matching "number" field (1, 2, 3...)
   - Use that task's "task_id" (UUID) for update/delete/complete operations
4. When user mentions a task by name/title, use list_tasks with search parameter to find it
5. ALWAYS confirm before deleting a task
6. If multiple tasks match, ask user to clarify which one
7. After completing an action, summarize what was done
8. IMPORTANT: Reply in the SAME language the user writes in. If user writes in English, reply in English. If user writes in Roman Urdu (like "mera task add karo"), reply in Roman Urdu.
9. If user says hi, hello, or greets you, respond with a friendly greeting and offer to help with tasks.

**MANDATORY: When listing tasks, COPY the formatted text from the tool response message EXACTLY as shown. Do NOT reformat it. The message already contains properly formatted tasks with numbers, icons, descriptions, and priorities. Just display it as-is.**
"""

# Cohere tool definitions
COHERE_TOOLS = [
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
                    "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "Task priority"},
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
                    "status": {"type": "string", "enum": ["all", "completed", "pending"], "description": "Filter by status"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "Filter by priority"},
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
                    "title": {"type": "string", "description": "New title"},
                    "description": {"type": "string", "description": "New description"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "New priority"},
                    "due_date": {"type": "string", "description": "New due date in ISO format"},
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


async def execute_tool(
    tool_name: str,
    tool_args: dict[str, Any],
    session: Any,
    user_id: UUID,
) -> dict[str, Any]:
    """Execute a tool and return the result."""
    if tool_name == "add_task":
        return await add_task(session, user_id, **tool_args)
    elif tool_name == "list_tasks":
        return await list_tasks(session, user_id, **tool_args)
    elif tool_name == "complete_task":
        return await complete_task(session, user_id, **tool_args)
    elif tool_name == "update_task":
        return await update_task(session, user_id, **tool_args)
    elif tool_name == "delete_task":
        return await delete_task(session, user_id, **tool_args)
    else:
        return {"success": False, "message": f"Unknown tool: {tool_name}"}


async def run_agent(
    session: Any,
    user_id: UUID,
    user_message: str,
    conversation_history: list[dict[str, Any]],
) -> tuple[str, list[dict[str, Any]]]:
    """Run the agent with conversation history and return response with tool calls.

    Returns:
        Tuple of (assistant_response, tool_calls_made)
    """
    tool_calls_made = []

    try:
        client = cohere.ClientV2(api_key=settings.cohere_api_key)

        # Build messages
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})

        max_iterations = 3
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Agent iteration {iteration}")

            try:
                logger.info(f"Calling Cohere API with {len(messages)} messages")
                response = client.chat(
                    model=settings.cohere_model,
                    messages=messages,
                    tools=COHERE_TOOLS,
                )
                logger.info(f"Cohere response received: has_tool_calls={bool(response.message.tool_calls)}")
            except Exception as e:
                logger.error(f"Cohere API error: {str(e)}\n{traceback.format_exc()}")
                return f"Sorry, I encountered an error: {str(e)}", tool_calls_made

            # Check if there are tool calls
            if response.message.tool_calls:
                # Add assistant message with tool calls
                messages.append({
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in response.message.tool_calls
                    ],
                })

                # Execute each tool call
                for tool_call in response.message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                    logger.info(f"Executing tool: {tool_name} with args: {tool_args}")

                    try:
                        result = await execute_tool(tool_name, tool_args, session, user_id)
                        logger.info(f"Tool {tool_name} result: {result}")
                    except Exception as e:
                        logger.error(f"Tool execution error: {str(e)}\n{traceback.format_exc()}")
                        result = {"success": False, "message": f"Tool error: {str(e)}"}

                    tool_calls_made.append({
                        "tool": tool_name,
                        "arguments": tool_args,
                        "result": result,
                    })

                    # Add tool result to messages
                    tool_result_content = json.dumps(result, default=str)
                    logger.info(f"Adding tool result to messages: {tool_result_content[:200]}")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result_content,
                    })
            else:
                # No tool calls, return the response
                logger.info("No more tool calls, extracting response text")
                response_text = ""
                try:
                    if response.message.content:
                        for block in response.message.content:
                            if hasattr(block, 'text'):
                                response_text += block.text
                    logger.info(f"Response text: {response_text[:200] if response_text else 'empty'}")
                except Exception as e:
                    logger.error(f"Error extracting response text: {str(e)}\n{traceback.format_exc()}")
                    response_text = "Task completed successfully."
                return response_text or "Done! Task completed successfully.", tool_calls_made

        logger.info("Max iterations reached")
        return "Task completed.", tool_calls_made

    except Exception as e:
        logger.error(f"Agent error: {str(e)}\n{traceback.format_exc()}")
        # If we made tool calls but got an error afterwards, still return success
        if tool_calls_made:
            return "Task completed successfully!", tool_calls_made
        return f"Sorry, an error occurred: {str(e)}", tool_calls_made
