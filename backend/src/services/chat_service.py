"""Chat service for conversation management and AI processing."""

import json
import logging
import traceback
from uuid import UUID
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.conversation import Conversation
from src.models.message import Message
from src.models.enums import MessageRole
from src.models.base import utcnow
from src.agent.todo_agent import run_agent

logger = logging.getLogger(__name__)


class ChatService:
    """Service for chat operations - stateless design."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, user_id: UUID, title: str | None = None) -> Conversation:
        """Create a new conversation for the user."""
        conversation = Conversation(user_id=user_id, title=title)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def get_conversation(self, conversation_id: UUID, user_id: UUID) -> Conversation | None:
        """Get a conversation by ID, validating user ownership."""
        result = await self.session.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def load_conversation_history(self, conversation_id: UUID) -> list[dict[str, Any]]:
        """Load conversation history as message list for agent context."""
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        messages = result.scalars().all()

        history = []
        for msg in messages:
            if msg.role == MessageRole.USER:
                history.append({"role": "user", "content": msg.content})
            elif msg.role == MessageRole.ASSISTANT:
                history.append({"role": "assistant", "content": msg.content})
        return history

    async def save_message(
        self,
        conversation_id: UUID,
        user_id: UUID,
        role: MessageRole,
        content: str,
        tool_calls: Any | None = None,
        tool_results: Any | None = None,
    ) -> Message:
        """Save a message to the conversation."""
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_results=tool_results,
        )
        self.session.add(message)

        # Update conversation's updated_at
        result = await self.session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if conversation:
            conversation.updated_at = utcnow()
            self.session.add(conversation)

        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def process_chat(
        self,
        user_id: UUID,
        message: str,
        conversation_id: UUID | None = None,
    ) -> tuple[UUID, str, list[dict[str, Any]]]:
        """Process a chat message - stateless flow.

        1. Load/create conversation
        2. Save user message
        3. Run agent
        4. Save assistant reply
        5. Return response

        Returns:
            Tuple of (conversation_id, response_text, tool_calls)
        """
        # Create or get conversation
        if conversation_id:
            conversation = await self.get_conversation(conversation_id, user_id)
            if not conversation:
                raise ValueError(f"Conversation not found: {conversation_id}")
        else:
            conversation = await self.create_conversation(user_id)

        # Load conversation history
        logger.info(f"Loading conversation history for {conversation.id}")
        history = await self.load_conversation_history(conversation.id)

        # Save user message
        logger.info(f"Saving user message: {message[:50]}...")
        await self.save_message(
            conversation_id=conversation.id,
            user_id=user_id,
            role=MessageRole.USER,
            content=message,
        )

        # Run agent
        logger.info("Running agent...")
        try:
            response_text, tool_calls = await run_agent(
                session=self.session,
                user_id=user_id,
                user_message=message,
                conversation_history=history,
            )
            logger.info(f"Agent returned: response_text={response_text[:100] if response_text else 'empty'}, tool_calls={len(tool_calls) if tool_calls else 0}")
        except Exception as e:
            logger.error(f"Agent error: {str(e)}\n{traceback.format_exc()}")
            raise

        # Save assistant message (serialize tool_calls for JSONB)
        logger.info("Serializing tool_calls for storage...")
        serialized_tool_calls = None
        if tool_calls:
            try:
                serialized_tool_calls = json.loads(json.dumps(tool_calls, default=str))
                logger.info(f"Serialized tool_calls: {str(serialized_tool_calls)[:200]}")
            except Exception as e:
                logger.error(f"Error serializing tool_calls: {str(e)}\n{traceback.format_exc()}")
                serialized_tool_calls = None

        logger.info("Saving assistant message...")
        await self.save_message(
            conversation_id=conversation.id,
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content=response_text,
            tool_calls=serialized_tool_calls,
        )

        logger.info("Chat processing complete")
        return conversation.id, response_text, tool_calls
