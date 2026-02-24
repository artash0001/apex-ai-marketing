"""
Apex AI Marketing - JWT Authentication

Provides login, token refresh, and route protection for the admin panel.
Validates against ADMIN_USERNAME / ADMIN_PASSWORD from settings.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# ── Password hashing ─────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Security scheme ───────────────────────────────────────────────────
security = HTTPBearer()


# ── Request / Response schemas ────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    username: str


class UserInfo(BaseModel):
    username: str
    role: str = "admin"


# ── Token helpers ─────────────────────────────────────────────────────

def _create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def _verify_token(token: str) -> dict:
    """Decode and verify a JWT token. Raises HTTPException on failure."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject",
            )
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {exc}",
        )


# ── Dependency: get current user ──────────────────────────────────────

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> UserInfo:
    """FastAPI dependency that extracts and validates the current user
    from the Authorization header.

    Usage in a route::

        @router.get("/protected")
        async def protected(user: UserInfo = Depends(get_current_user)):
            return {"message": f"Hello {user.username}"}
    """
    payload = _verify_token(credentials.credentials)
    return UserInfo(
        username=payload["sub"],
        role=payload.get("role", "admin"),
    )


# ── Routes ────────────────────────────────────────────────────────────

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    """Authenticate with username/password and receive a JWT token.

    Currently validates against the static admin credentials in settings.
    """
    if body.username != settings.ADMIN_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Compare passwords. Support both plain-text and hashed passwords.
    password_valid = False
    if body.password == settings.ADMIN_PASSWORD:
        password_valid = True
    elif pwd_context.identify(settings.ADMIN_PASSWORD):
        # The stored password looks like a hash
        password_valid = pwd_context.verify(body.password, settings.ADMIN_PASSWORD)

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    expires_delta = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = _create_access_token(
        data={"sub": body.username, "role": "admin"},
        expires_delta=expires_delta,
    )

    logger.info("Admin login: user=%s", body.username)

    return TokenResponse(
        access_token=access_token,
        expires_in=settings.JWT_EXPIRE_MINUTES * 60,
        username=body.username,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    user: UserInfo = Depends(get_current_user),
):
    """Refresh the JWT token. Requires a valid existing token."""
    expires_delta = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    new_token = _create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=expires_delta,
    )

    logger.info("Token refreshed for user=%s", user.username)

    return TokenResponse(
        access_token=new_token,
        expires_in=settings.JWT_EXPIRE_MINUTES * 60,
        username=user.username,
    )


@router.get("/me", response_model=UserInfo)
async def get_me(user: UserInfo = Depends(get_current_user)):
    """Return info about the currently authenticated user."""
    return user
