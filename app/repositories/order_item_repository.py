from sqlalchemy.orm import Session

from app.models.order_item import OrderItem


class OrderItemRepository:

    @staticmethod
    def create(
        db: Session,
        order_item: OrderItem
    ):
        db.add(order_item)
        db.flush()

        return order_item

    @staticmethod
    def get_order_items(
        db: Session,
        order_id: int
    ):
        return (
            db.query(OrderItem)
            .filter(
                OrderItem.order_id == order_id
            )
            .all()
        )