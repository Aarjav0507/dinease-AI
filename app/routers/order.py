from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.auth import get_current_user

from app.services.order_service import OrderService

from app.schemas.order import (
    CheckoutRequest,
    OrderResponse
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/checkout",
    response_model=OrderResponse
)
def checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Creates an order from
    reservation + cart items
    """

    return (
        OrderService.create_order_from_reservation(
            db,
            request.reservation_id,
            current_user
        )
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get order by id
    """

    return (
        OrderService.get_order_by_id(
            db,
            order_id,
            current_user
        )
    )


@router.get(
    "/my-orders",
    response_model=list[OrderResponse]
)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get all orders of current user
    """

    return (
        OrderService.get_my_orders(
            db,
            current_user
        )
    )