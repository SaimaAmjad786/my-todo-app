"""API versioning router with /api/v1 prefix."""

from fastapi import APIRouter

from src.api.routes.auth import router as auth_router
from src.api.routes.todos import router as todos_router
from src.api.routes.tags import router as tags_router
from src.api.routes.chat import router as chat_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(todos_router)
api_router.include_router(tags_router)
api_router.include_router(chat_router)
