from sqlalchemy.orm import Session

from app.models.order import Order


class OrderRepository:

    @staticmethod
    def create(
        db: Session,
        order: Order
    ):
        db.add(order)
        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def get_by_id(
        db: Session,
        order_id: int
    ):
        return (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    @staticmethod
    def get_by_reservation_id(
        db: Session,
        reservation_id: int
    ):
        return (
            db.query(Order)
            .filter(
                Order.reservation_id == reservation_id
            )
            .first()
        )

    @staticmethod
    def get_user_orders(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Order)
            .filter(
                Order.user_id == user_id
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        order: Order
    ):
        db.commit()
        db.refresh(order)

        return order
    @staticmethod
    def get_all_orders(
     db: Session
):
      return (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .all()
    )


    @staticmethod
    def update_order(
      db: Session,
      order: Order
):
      db.commit()
      db.refresh(order)

      return order
    @staticmethod
    def count_orders(
       db: Session
):
       return db.query(Order).count()