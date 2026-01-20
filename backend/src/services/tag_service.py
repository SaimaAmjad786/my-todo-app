"""Tag service for business logic and data access."""

from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.tag import Tag


class TagService:
    """Service for tag CRUD operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_tags(self, user_id: UUID) -> list[Tag]:
        """List all tags for a user.

        Args:
            user_id: Owner's user ID

        Returns:
            List of tags
        """
        result = await self.session.execute(
            select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        )
        return list(result.scalars().all())

    async def get_tag(self, tag_id: UUID, user_id: UUID) -> Tag | None:
        """Get a tag by ID for a specific user.

        Args:
            tag_id: Tag ID
            user_id: Owner's user ID

        Returns:
            Tag if found and owned by user, None otherwise
        """
        result = await self.session.execute(
            select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_tag_by_name(self, name: str, user_id: UUID) -> Tag | None:
        """Get a tag by name for a specific user.

        Args:
            name: Tag name
            user_id: Owner's user ID

        Returns:
            Tag if found, None otherwise
        """
        result = await self.session.execute(
            select(Tag).where(Tag.name == name, Tag.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_tag(self, user_id: UUID, name: str) -> Tag:
        """Create a new tag.

        Args:
            user_id: Owner's user ID
            name: Tag name

        Returns:
            Created tag
        """
        tag = Tag(user_id=user_id, name=name)
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def delete_tag(self, tag: Tag) -> None:
        """Delete a tag.

        Args:
            tag: Tag to delete
        """
        await self.session.delete(tag)
        await self.session.commit()
