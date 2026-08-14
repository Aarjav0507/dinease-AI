from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
)
from app.services.user_service import UserService
from app.schemas.auth import (
    ForgotPasswordRequest,
    ResetPasswordRequest
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """

    return UserService.register_user(
        db=db,
        user_data=user
    )

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK
)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return a JWT token.
    """

    return UserService.login_user(
        db=db,
        login_data=login_data
    )
@router.post(
    "/forgot-password"
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    return (
        UserService.forgot_password(
            db,
            request.email
        )
    )
@router.post(
    "/reset-password"
)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    return (
        UserService.reset_password(
            db,
            request.token,
            request.new_password
        )
    )