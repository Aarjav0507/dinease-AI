from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cart_item import CartItem

from app.schemas.cart import (
    AddToCartRequest,
    UpdateCartItemRequest
)

from app.repositories.cart_repository import (
    CartRepository
)

from app.repositories.menu_item_repository import (
    MenuItemRepository
)


class CartService:

    @staticmethod
    def add_to_cart(
        db: Session,
        user_id: int,
        request: AddToCartRequest
    ):

        # Check menu item exists
        menu_item = MenuItemRepository.get_by_id(
            db,
            request.menu_item_id
        )

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        # Get user's cart
        cart = CartRepository.get_by_user_id(
            db,
            user_id
        )

        # Create cart if it doesn't exist
        if not cart:
            cart = CartRepository.create_cart(
                db,
                user_id
            )

        # Check if item already exists in cart
        existing_item = CartRepository.get_cart_item(
            db,
            cart.id,
            request.menu_item_id
        )

        if existing_item:
            existing_item.quantity += request.quantity

            return CartRepository.update_cart_item(
                db,
                existing_item
            )

        # Create new cart item
        cart_item = CartItem(
            cart_id=cart.id,
            menu_item_id=request.menu_item_id,
            quantity=request.quantity
        )

        return CartRepository.add_cart_item(
            db,
            cart_item
        )

    @staticmethod
    def get_cart(
        db: Session,
        user_id: int
    ):

        cart = CartRepository.get_by_user_id(
            db,
            user_id
        )

        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found."
            )

        return cart

    @staticmethod
    def update_cart_item(
        db: Session,
        cart_item_id: int,
        request: UpdateCartItemRequest
    ):

        cart_item = (
            db.query(CartItem)
            .filter(
                CartItem.id == cart_item_id
            )
            .first()
        )

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found."
            )

        cart_item.quantity = request.quantity

        return CartRepository.update_cart_item(
            db,
            cart_item
        )

    @staticmethod
    def remove_cart_item(
        db: Session,
        cart_item_id: int
    ):

        cart_item = (
            db.query(CartItem)
            .filter(
                CartItem.id == cart_item_id
            )
            .first()
        )

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found."
            )

        CartRepository.delete_cart_item(
            db,
            cart_item
        )

        return {
            "message": "Cart item removed successfully."
        }