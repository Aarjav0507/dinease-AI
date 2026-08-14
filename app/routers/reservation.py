from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.reservation import (
    ReservationCreate,
    ReservationResponse
)

from app.services.reservation_service import (
    ReservationService
)

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.post(
    "/",
    response_model=ReservationResponse
)
def create_reservation(
    reservation_data: ReservationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return ReservationService.create_reservation(
        db=db,
        user_id=current_user.id,
        reservation_data=reservation_data
    )


@router.get(
    "/me",
    response_model=List[ReservationResponse]
)
def get_my_reservations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return ReservationService.get_user_reservations(
        db,
        current_user.id
    )


@router.get(
    "/{reservation_id}",
    response_model=ReservationResponse
)
def get_reservation_by_id(
    reservation_id: int,
    db: Session = Depends(get_db)
):

    return ReservationService.get_reservation_by_id(
        db,
        reservation_id
    )


@router.get(
    "/",
    response_model=List[ReservationResponse]
)
def get_all_reservations(
    db: Session = Depends(get_db)
):

    return ReservationService.get_all_reservations(
        db
    )
@router.post("/{reservation_id}/cancel")
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return ReservationService.cancel_reservation(
        db,
        reservation_id,
        current_user
    )