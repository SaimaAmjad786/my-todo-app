"""Database configuration with async SQLModel engine for Neon PostgreSQL."""

from collections.abc import AsyncGenerator
from datetime import datetime
from enum import Enum
from urllib.parse import urlparse

from sqlalchemy import DateTime, Enum as SAEnum, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TypeDecorator
from sqlmodel import SQLModel

from src.core.config import get_settings

settings = get_settings()


class PydanticEnumType(TypeDecorator):
    """Type decorator for Pydantic Enum to work with asyncpg."""

    impl = String
    cache_ok = True

    def __init__(self, enum_class: type[Enum], **kwargs):
        super().__init__(**kwargs)
        self.enum_class = enum_class

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            return value.value if isinstance(value, Enum) else str(value)
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            try:
                return self.enum_class(value)
            except ValueError:
                return value
        return process

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(String())


# Parse URL for asyncpg
url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
parsed_url = urlparse(url)

# Create async engine for Neon PostgreSQL with SSL
engine = create_async_engine(
    f"postgresql+asyncpg://{parsed_url.netloc}{parsed_url.path}",
    echo=settings.debug,
    future=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={"ssl": "require"},
)

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_db_and_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
