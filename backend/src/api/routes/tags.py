"""Tag API routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.deps.auth import CurrentUser
from src.api.schemas.tag import CreateTagRequest, TagResponse
from src.core.database import get_session
from src.services.tag_service import TagService

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("", response_model=list[TagResponse])
async def list_tags(
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[TagResponse]:
    """List all tags for the current user."""
    service = TagService(session)
    tags = await service.list_tags(user_id=current_user.id)
    return [TagResponse.model_validate(tag, from_attributes=True) for tag in tags]


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    request: CreateTagRequest,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagResponse:
    """Create a new tag."""
    service = TagService(session)

    # Check if tag with same name exists
    existing = await service.get_tag_by_name(name=request.name, user_id=current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag with this name already exists",
        )

    tag = await service.create_tag(user_id=current_user.id, name=request.name)
    return TagResponse.model_validate(tag, from_attributes=True)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: UUID,
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    """Delete a tag."""
    service = TagService(session)
    tag = await service.get_tag(tag_id=tag_id, user_id=current_user.id)

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    await service.delete_tag(tag)
