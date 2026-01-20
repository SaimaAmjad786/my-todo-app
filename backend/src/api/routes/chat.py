"""Chat API routes for AI chatbot."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.deps.auth import CurrentUser
from src.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationInfo,
    ConversationListResponse,
    ConversationDetailResponse,
    MessageInfo,
    ToolCall,
)
from src.core.database import get_session
from src.models.conversation import Conversation
from src.models.message import Message
from src.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ChatResponse:
    """Send a message to the AI assistant.

    Args:
        request: Chat request with message and optional conversation_id
        current_user: The authenticated user
        session: Database session

    Returns:
        ChatResponse with assistant response and tool calls

    Raises:
        HTTPException: 404 if conversation not found
        HTTPException: 500 if AI processing fails
    """
    service = ChatService(session)

    try:
        conversation_id, response_text, tool_calls = await service.process_chat(
            user_id=current_user.id,
            message=request.message,
            conversation_id=request.conversation_id,
        )

        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            tool_calls=[ToolCall(**tc) for tc in tool_calls] if tool_calls else [],
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}",
        )


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ConversationListResponse:
    """List all conversations for the current user.

    Args:
        current_user: The authenticated user
        session: Database session

    Returns:
        List of conversations ordered by most recent
    """
    result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
    )
    conversations = result.scalars().all()

    return ConversationListResponse(
        conversations=[ConversationInfo.model_validate(c) for c in conversations],
        total=len(conversations),
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: UUID,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ConversationDetailResponse:
    """Get a conversation with all its messages.

    Args:
        conversation_id: The conversation UUID
        current_user: The authenticated user
        session: Database session

    Returns:
        Conversation details with all messages

    Raises:
        HTTPException: 404 if conversation not found
    """
    result = await session.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    # Get messages
    messages_result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = messages_result.scalars().all()

    return ConversationDetailResponse(
        conversation=ConversationInfo.model_validate(conversation),
        messages=[
            MessageInfo(
                id=m.id,
                role=m.role.value,
                content=m.content,
                tool_calls=[ToolCall(**tc) for tc in m.tool_calls] if m.tool_calls else None,
                created_at=m.created_at,
            )
            for m in messages
        ],
    )


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: UUID,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    """Delete a conversation and all its messages.

    Args:
        conversation_id: The conversation UUID
        current_user: The authenticated user
        session: Database session

    Raises:
        HTTPException: 404 if conversation not found
    """
    result = await session.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    await session.delete(conversation)
    await session.commit()
