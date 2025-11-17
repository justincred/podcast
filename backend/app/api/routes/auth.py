"""
Authentication API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models import User
from app.schemas.user import UserRegister, UserLogin, UserWithToken, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.api.deps import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserWithToken, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    Args:
        user_data: User registration data (email, password, full_name)
        db: Database session

    Returns:
        User data with JWT access token

    Raises:
        HTTPException: If email already exists
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return UserWithToken(
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            tier=user.tier,
            monthly_uploads_used=user.monthly_uploads_used,
            uploads_remaining=user.uploads_remaining,
            created_at=user.created_at,
        ),
        access_token=access_token,
    )


@router.post("/login", response_model=UserWithToken)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Login with email and password.

    Args:
        credentials: Login credentials (email, password)
        db: Database session

    Returns:
        User data with JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Generate access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return UserWithToken(
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            tier=user.tier,
            monthly_uploads_used=user.monthly_uploads_used,
            uploads_remaining=user.uploads_remaining,
            created_at=user.created_at,
        ),
        access_token=access_token,
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Get current authenticated user information.

    Args:
        current_user: Current authenticated user from JWT token

    Returns:
        User data
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        tier=current_user.tier,
        monthly_uploads_used=current_user.monthly_uploads_used,
        uploads_remaining=current_user.uploads_remaining,
        created_at=current_user.created_at,
    )
