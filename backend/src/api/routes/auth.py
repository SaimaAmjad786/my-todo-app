"""Authentication API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.deps.auth import CurrentUser
from src.api.schemas.auth import (
    AuthResponse,
    MessageResponse,
    SigninRequest,
    SignupRequest,
    UserResponse,
)
from src.core.auth import create_access_token, get_password_hash, verify_password
from src.core.database import get_session
from src.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthResponse:
    """Register a new user account.

    Args:
        request: Signup request with email, password, and optional name
        session: Database session

    Returns:
        AuthResponse with access token and user data

    Raises:
        HTTPException: 409 if email already exists
    """
    # Check if email already exists
    result = await session.execute(select(User).where(User.email == request.email))
    existing_user = result.unique().scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create new user
    user = User(
        email=request.email,
        name=request.name,
        hashed_password=get_password_hash(request.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Initialize default tags for new user
    from src.models.tag import Tag
    default_tags = ["Category", "Work", "Shopping"]
    for tag_name in default_tags:
        tag = Tag(user_id=user.id, name=tag_name)
        session.add(tag)
    await session.commit()

    # Generate access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return AuthResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/signin", response_model=AuthResponse)
async def signin(
    request: SigninRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthResponse:
    """Authenticate user and return access token.

    Args:
        request: Signin request with email and password
        session: Database session

    Returns:
        AuthResponse with access token and user data

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Find user by email
    result = await session.execute(select(User).where(User.email == request.email))
    user = result.unique().scalar_one_or_none()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return AuthResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/signout", response_model=MessageResponse)
async def signout(current_user: CurrentUser) -> MessageResponse:
    """Sign out current user.

    Note: JWT tokens are stateless, so signout is handled client-side
    by removing the token. This endpoint exists for API consistency.

    Args:
        current_user: The authenticated user

    Returns:
        Success message
    """
    return MessageResponse(message="Successfully signed out")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser) -> UserResponse:
    """Get current authenticated user information.

    Args:
        current_user: The authenticated user

    Returns:
        Current user data
    """
    return UserResponse.model_validate(current_user)
