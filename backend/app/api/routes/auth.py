import uuid
from typing import Annotated
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import create_access_token
from app.models import User
from app.schemas.auth import TokenResponse, TokenVerifyResponse, UserResponse

router = APIRouter()
settings = get_settings()


# ============== GitHub OAuth ==============


@router.get("/github")
async def github_login() -> RedirectResponse:
    """Redirect to GitHub OAuth."""
    if not settings.github_client_id:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth not configured",
        )

    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": f"{settings.backend_url}/api/auth/github/callback",
        "scope": "read:user user:email",
    }
    url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url=url)


@router.get("/github/callback")
async def github_callback(
    code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RedirectResponse:
    """Handle GitHub OAuth callback."""
    if not settings.github_client_id or not settings.github_client_secret:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth not configured",
        )

    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        token_data = token_response.json()

        if "access_token" not in token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get access token from GitHub",
            )

        access_token = token_data["access_token"]

        # Get user info
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        github_user = user_response.json()

        # Get user email if not public
        email = github_user.get("email")
        if not email:
            emails_response = await client.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            emails = emails_response.json()
            primary_email = next(
                (e for e in emails if e.get("primary") and e.get("verified")), None
            )
            if primary_email:
                email = primary_email["email"]

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not get email from GitHub",
        )

    # Find or create user
    user = await _get_or_create_user(
        db=db,
        email=email,
        name=github_user.get("name") or github_user.get("login"),
        avatar=github_user.get("avatar_url"),
        provider="github",
        provider_id=str(github_user["id"]),
    )

    # Create JWT token
    jwt_token = create_access_token(data={"sub": user.id})

    # Redirect to frontend with token
    user_data = UserResponse.model_validate(user).model_dump_json()
    redirect_url = f"{settings.frontend_url}?token={jwt_token}&user={user_data}"
    return RedirectResponse(url=redirect_url)


# ============== Google OAuth ==============


@router.get("/google")
async def google_login() -> RedirectResponse:
    """Redirect to Google OAuth."""
    if not settings.google_client_id:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured",
        )

    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": f"{settings.backend_url}/api/auth/google/callback",
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url=url)


@router.get("/google/callback")
async def google_callback(
    code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RedirectResponse:
    """Handle Google OAuth callback."""
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured",
        )

    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": f"{settings.backend_url}/api/auth/google/callback",
            },
        )
        token_data = token_response.json()

        if "access_token" not in token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get access token from Google",
            )

        access_token = token_data["access_token"]

        # Get user info
        user_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        google_user = user_response.json()

    email = google_user.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not get email from Google",
        )

    # Find or create user
    user = await _get_or_create_user(
        db=db,
        email=email,
        name=google_user.get("name"),
        avatar=google_user.get("picture"),
        provider="google",
        provider_id=google_user["id"],
    )

    # Create JWT token
    jwt_token = create_access_token(data={"sub": user.id})

    # Redirect to frontend with token
    user_data = UserResponse.model_validate(user).model_dump_json()
    redirect_url = f"{settings.frontend_url}?token={jwt_token}&user={user_data}"
    return RedirectResponse(url=redirect_url)


# ============== Token Verification ==============


@router.get("/verify", response_model=TokenVerifyResponse)
async def verify_token(
    current_user: Annotated[User, Depends(get_current_user)],
) -> TokenVerifyResponse:
    """Verify JWT token and return user info."""
    return TokenVerifyResponse(
        valid=True,
        user=UserResponse.model_validate(current_user),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Get current user info."""
    return UserResponse.model_validate(current_user)


# ============== Helper Functions ==============


async def _get_or_create_user(
    db: AsyncSession,
    email: str,
    name: str,
    avatar: str | None,
    provider: str,
    provider_id: str,
) -> User:
    """Get existing user or create new one."""
    # Try to find by email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        # Update user info
        user.name = name
        user.avatar = avatar
        await db.flush()
        return user

    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=email,
        name=name,
        avatar=avatar,
        provider=provider,
        provider_id=provider_id,
        role="admin" if await _is_first_user(db) else "user",
    )
    db.add(user)
    await db.flush()
    return user


async def _is_first_user(db: AsyncSession) -> bool:
    """Check if this is the first user (will be admin)."""
    result = await db.execute(select(User).limit(1))
    return result.scalar_one_or_none() is None
