from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import create_access_token, get_current_user
from src.models.user import User
from src.schemas.user import AuthResponse, UserCreate, UserLogin, UserResponse
from src.schemas.wallet import WalletResponse
from src.services.auth_service import login_user, register_user

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]) -> AuthResponse:
    user = register_user(db, user_data)
    return AuthResponse(
        access_token=create_access_token(str(user.id)),
        user=user,
    )


@router.post("/login", response_model=AuthResponse)
def login(credentials: UserLogin, db: Annotated[Session, Depends(get_db)]) -> AuthResponse:
    token, user = login_user(db, credentials.username, credentials.password)
    return AuthResponse(access_token=token, user=user)


@router.get("/me", response_model=UserResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.get("/wallet", response_model=WalletResponse)
def wallet(current_user: Annotated[User, Depends(get_current_user)]) -> WalletResponse:
    if current_user.wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        )
    return current_user.wallet
