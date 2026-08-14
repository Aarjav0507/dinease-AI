from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user

from app.services.payment_service import PaymentService
from app.schemas.payment import (PaymentVerifyRequest)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/create/{order_id}")
def create_payment(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PaymentService.create_payment(
        db,
        order_id,
        current_user
    )
@router.post("/verify")
def verify_payment(
    payment_data: PaymentVerifyRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return PaymentService.verify_payment(
        db,
        payment_data,
        current_user
    )
@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return PaymentService.get_payment_by_id(
        db,
        payment_id,
        current_user
    )