from fastapi import Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.core.constants import ADMIN_ROLE


def admin_required(
    current_user = Depends(get_current_user)
):

    if current_user.role != ADMIN_ROLE:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user