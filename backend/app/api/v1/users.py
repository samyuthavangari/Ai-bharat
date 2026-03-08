"""
JanSahay AI - User & Auth API Routes
Registration, login, profile management.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.database import get_db
from app.models.user import User
from app.auth.oauth2 import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    get_current_user, require_auth,
)
from app.schemas import (
    UserRegister, UserLogin, TokenResponse,
    UserProfile, UserProfileUpdate, APIResponse,
)

router = APIRouter(prefix="/users", tags=["Users & Auth"])


@router.post("/register", response_model=APIResponse)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register a new citizen account."""
    # Check existing
    query = select(User)
    if data.email:
        query = query.where(User.email == data.email)
    elif data.phone_number:
        query = query.where(User.phone_number == data.phone_number)
    else:
        raise HTTPException(400, "Email or phone number required")

    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(400, "User already exists with this email/phone")

    user = User(
        phone_number=data.phone_number,
        email=data.email,
        full_name=data.full_name,
        password_hash=hash_password(data.password),
        preferred_language=data.preferred_language,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    tokens = _generate_tokens(user)
    return APIResponse(success=True, message="Registration successful", data=tokens)


@router.post("/login", response_model=APIResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login with email/phone and password."""
    result = await db.execute(
        select(User).where(
            or_(User.email == data.username, User.phone_number == data.username)
        )
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    tokens = _generate_tokens(user)
    return APIResponse(success=True, message="Login successful", data=tokens)


@router.get("/profile", response_model=UserProfile)
async def get_profile(user: User = Depends(require_auth)):
    """Get current user's profile."""
    return user


@router.put("/profile", response_model=APIResponse)
async def update_profile(
    data: UserProfileUpdate,
    user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Update user profile (demographics for scheme matching)."""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    await db.flush()
    return APIResponse(success=True, message="Profile updated successfully")


def _generate_tokens(user: User) -> dict:
    return {
        "access_token": create_access_token({"sub": str(user.id), "role": user.role.value}),
        "refresh_token": create_refresh_token({"sub": str(user.id)}),
        "token_type": "bearer",
        "user_id": user.id,
    }
