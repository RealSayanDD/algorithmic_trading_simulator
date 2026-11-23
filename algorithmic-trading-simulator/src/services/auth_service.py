
from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.config import get_settings
from src.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from src.models.user import User
from src.models.wallet import Wallet
from src.schemas.user import UserCreate


def register_user(db: Session, user_data: UserCreate) -> User:
    # Check whether email or username already exists
    existing_user = db.scalar(
        select(User).where(
            or_(
                User.email == user_data.email,
                User.username == user_data.username,
            )
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username is already registered",
        )

    # Create new user
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
    )

    # Automatically create a virtual wallet
    user.wallet = Wallet(
        balance=get_settings().initial_wallet_balance
    )

    db.add(user)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username is already registered",
        ) from None

    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User:

    user = db.scalar(
        select(User).where(User.username == username)
    )

    # Validate credentials
    if user is None or not verify_password(
        password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check whether account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    return user


def login_user(
    db: Session,
    username: str,
    password: str,
) -> tuple[str, User]:

    user = authenticate_user(
        db,
        username,
        password,
    )

    token = create_access_token(str(user.id))

    return token, user
