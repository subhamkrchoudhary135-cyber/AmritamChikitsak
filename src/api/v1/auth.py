"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_current_user, get_db
from src.core.audit import audit_logger
from src.core.config import settings
from src.core.crypto import pii_crypto
from src.core.security import (
    UserRole,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from src.db.models import Patient, User
from src.schemas.auth import RefreshTokenRequest, Token, UserRegister, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user account with DPDP Act encrypted patient profile."""
    # Check if user already exists
    stmt = select(User).where((User.email == payload.email) | (User.username == payload.username))
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists",
        )

    # Create user
    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=get_password_hash(payload.password),
        role=payload.role.value if isinstance(payload.role, UserRole) else str(payload.role),
        is_active=True,
        is_verified=False,
    )
    db.add(user)
    await db.flush()

    # If role is patient and identity fields supplied, create Patient entity with encrypted PII
    if payload.role == UserRole.PATIENT and payload.full_name and payload.phone_number:
        patient = Patient(
            user_id=user.id,
            full_name=payload.full_name,
            phone_number=payload.phone_number,
            abha_id=payload.abha_id,
            age=payload.age or 35,
            gender=payload.gender or "other",
            preferred_language=payload.preferred_language or "en",
            phone_blind_index=pii_crypto.compute_blind_index(payload.phone_number),
            email_blind_index=pii_crypto.compute_blind_index(payload.email),
        )
        db.add(patient)

    await db.commit()
    await db.refresh(user)

    audit_logger.log_event(
        action="USER_REGISTERED",
        user_id=user.id,
        role=user.role,
        resource_type="USER",
        resource_id=user.id,
    )

    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """OAuth2 password login granting JWT access and refresh tokens."""
    stmt = select(User).where(
        (User.username == form_data.username) | (User.email == form_data.username)
    )
    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        audit_logger.log_event(
            action="USER_LOGIN_FAILED",
            user_id=user.id if user else "UNKNOWN",
            status="FAILED",
            details={"attempted_username": form_data.username[:3] + "***"},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    access_token = create_access_token(
        subject=user.id,
        role=UserRole(user.role),
        extra_claims={"email": user.email, "username": user.username},
    )
    refresh_token = create_refresh_token(subject=user.id, role=UserRole(user.role))

    audit_logger.log_event(
        action="USER_LOGIN_SUCCESS",
        user_id=user.id,
        role=user.role,
        resource_type="AUTH",
        resource_id=user.id,
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        role=user.role,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    payload: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Generate a new access token using a valid refresh token."""
    decoded = decode_token(payload.refresh_token)
    if decoded is None or decoded.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id = decoded.get("sub")
    stmt = select(User).where(User.id == user_id)
    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer active or valid",
        )

    new_access_token = create_access_token(
        subject=user.id,
        role=UserRole(user.role),
        extra_claims={"email": user.email, "username": user.username},
    )
    new_refresh_token = create_refresh_token(subject=user.id, role=UserRole(user.role))

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        role=user.role,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    """Retrieve profile of currently authenticated user."""
    return current_user
