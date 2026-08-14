from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas import user
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository
from app.auth.hashing import hash_password
from app.auth.hashing import verify_password
from app.auth.jwt_handler import create_access_token
from app.schemas.user import UserLogin, Token
from datetime import datetime

from fastapi import HTTPException
from app.auth.hashing import hash_password
import secrets

from datetime import datetime
from datetime import timedelta

from app.services.notification_service import NotificationService

class UserService:

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserCreate
    ) -> User:
        """
        Register a new user.
        """

        # Check if email already exists
        existing_user = UserRepository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

        existing_phone = UserRepository.get_by_phone_number(
            db,
            user_data.phone_number
        )

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered."
            )

        # Create User object
        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            password=hash_password(user_data.password),
            role="customer",
            is_active=True,
        )

        return UserRepository.create(
            db,
            new_user
        )
    @staticmethod
    def login_user(
       db: Session,
       login_data: UserLogin
) -> Token:
       """Authenticate a user and return a JWT token."""

       # Step 1: Find user by email
       user = UserRepository.get_by_email(db, login_data.email)

       # Step 2: Check if user exists
       if not user:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid email or password."
           )

       # Step 3: Verify password
       if not verify_password(login_data.password, user.password):
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid email or password."
           )

       # Step 4: Generate JWT
       token = create_access_token({"sub": user.email})

       # Step 5: Return token
       return Token(access_token=token, token_type="bearer")
    @staticmethod
    def forgot_password(
      db: Session,
      email: str
):

      user = UserRepository.get_by_email(
        db,
        email
    )

      if not user:
        return {
            "message":
            "If the email exists, a reset link has been sent."
        }

      token = secrets.token_urlsafe(32)

      user.password_reset_token = token

      user.password_reset_token_expiry = (
        datetime.utcnow()
        + timedelta(minutes=15)
    )

      UserRepository.update(
        db,
        user
    )

      reset_link = (
        f"http://localhost:5173/reset-password"
        f"?token={token}"
    )

      NotificationService.send_password_reset_email(
        user.email,
        reset_link
    )

      return {
        "message":
        "Password reset email sent successfully."
    }
    @staticmethod
    def reset_password(
      db: Session,
      token: str,
      new_password: str
):

      user = (
        UserRepository.get_by_reset_token(
            db,
            token
        )
    )

      if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid reset token"
        )

      if (
        user.password_reset_token_expiry is None
        or datetime.utcnow()
        > user.password_reset_token_expiry
    ):
        raise HTTPException(
            status_code=400,
            detail="Reset token expired"
        )

      user.password = hash_password(
        new_password
    )

      user.password_reset_token = None

      user.password_reset_token_expiry = None

      UserRepository.update(
        db,
        user
    )

      return {
        "message":
        "Password reset successful"
    }
   


