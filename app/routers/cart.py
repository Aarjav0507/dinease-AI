from fastapi import (
    APIRouter,
    Depends,
    status
)
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.cart import (
    AddToCartRequest,
    UpdateCartItemRequest,
    CartResponse,
    CartItemResponse
)

from app.services.cart_service import (
    CartService
)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post(
    "/add",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED
)
def add_to_cart(
    request: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CartService.add_to_cart(
        db=db,
        user_id=current_user.id,
        request=request
    )


@router.get(
    "/",
    response_model=CartResponse
)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CartService.get_cart(
        db=db,
        user_id=current_user.id
    )


@router.put(
    "/item/{cart_item_id}",
    response_model=CartItemResponse
)
def update_cart_item(
    cart_item_id: int,
    request: UpdateCartItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CartService.update_cart_item(
        db=db,
        cart_item_id=cart_item_id,
        request=request
    )


@router.delete(
    "/item/{cart_item_id}"
)
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CartService.remove_cart_item(
        db=db,
        cart_item_id=cart_item_id
    )