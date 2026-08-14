from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth.jwt_handler import verify_access_token
from app.repositories.user_repository import UserRepository

from fastapi.security import HTTPBearer

security = HTTPBearer()

from fastapi.security import HTTPAuthorizationCredentials

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Verify JWT token and return the currently authenticated user.
    """

    # Step 1: Verify JWT token
    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    # Step 2: Extract email from JWT payload
    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )

    # Step 3: Find user in database
    user = UserRepository.get_by_email(
        db=db,
        email=email
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )

    # Step 4: Return authenticated user
    return user