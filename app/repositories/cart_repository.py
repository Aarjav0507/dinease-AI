from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem


class CartRepository:

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Cart)
            .filter(Cart.user_id == user_id)
            .first()
        )

    @staticmethod
    def create_cart(
        db: Session,
        user_id: int
    ) -> Cart:

        cart = Cart(
            user_id=user_id
        )

        db.add(cart)
        db.commit()
        db.refresh(cart)

        return cart

    @staticmethod
    def get_cart_item(
        db: Session,
        cart_id: int,
        menu_item_id: int
    ):
        return (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.menu_item_id == menu_item_id
            )
            .first()
        )

    @staticmethod
    def add_cart_item(
        db: Session,
        cart_item: CartItem
    ) -> CartItem:

        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)

        return cart_item

    @staticmethod
    def update_cart_item(
        db: Session,
        cart_item: CartItem
    ) -> CartItem:

        db.commit()
        db.refresh(cart_item)

        return cart_item

    @staticmethod
    def delete_cart_item(
        db: Session,
        cart_item: CartItem
    ):

        db.delete(cart_item)
        db.commit()

    @staticmethod
    def get_cart_by_id(
        db: Session,
        cart_id: int
    ):
        return (
            db.query(Cart)
            .filter(Cart.id == cart_id)
            .first()
        )
    @staticmethod
    def get_cart_items(
        db: Session,
        cart_id: int
):
        return (
           db.query(CartItem)
            .filter(
              CartItem.cart_id == cart_id
        )
            .all()
    )
    @staticmethod
    def clear_cart(
        db: Session,
        cart_id: int
):

     (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart_id
        )
        .delete()
    )