from fastapi import (
    Depends,
    HTTPException,
    status
)

from app.dependencies.auth import (
    get_current_user
)
from app.core.constants import (
    ADMIN_ROLE
)

def get_current_admin(
    current_user=Depends(
        get_current_user
    )
):
    if current_user.role.lower() != ADMIN_ROLE.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user