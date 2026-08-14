from sqlalchemy.orm import Session

from app.models.payment import Payment
from sqlalchemy import func

class PaymentRepository:

    @staticmethod
    def create(
        db: Session,
        payment: Payment
    ) -> Payment:

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return payment

    @staticmethod
    def get_by_id(
        db: Session,
        payment_id: int
    ):

        return (
            db.query(Payment)
            .filter(
                Payment.id == payment_id
            )
            .first()
        )

    @staticmethod
    def get_by_order_id(
        db: Session,
        order_id: int
    ):

        return (
            db.query(Payment)
            .filter(
                Payment.order_id == order_id
            )
            .first()
        )

    @staticmethod
    def get_by_razorpay_order_id(
        db: Session,
        razorpay_order_id: str
    ):

        return (
            db.query(Payment)
            .filter(
                Payment.razorpay_order_id == razorpay_order_id
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        payment: Payment
    ) -> Payment:

        db.commit()
        db.refresh(payment)

        return payment
    @staticmethod
    def get_by_payment_id(
       db: Session,
       razorpay_payment_id: str
):
        return (
         db.query(Payment)
         .filter(
            Payment.razorpay_payment_id == razorpay_payment_id
         )
         .first()
    )
    @staticmethod
    def count_payments(
       db: Session
):
       return db.query(Payment).count()
    @staticmethod
    def total_revenue(
        db: Session
):
     return (
        db.query(
            func.sum(Payment.amount)
        )
        .filter(
            Payment.payment_status == "PAID"
        )
        .scalar()
        or 0
    )
    @staticmethod
    def get_gross_revenue(
       db: Session
):
      return (
        db.query(
            func.sum(Payment.amount)
        )
        .filter(
            Payment.payment_status == "PAID"
        )
        .scalar()
        or 0
    )
    @staticmethod
    def get_total_refund_amount(
      db: Session
):
      return (
        db.query(
            func.sum(Payment.refund_amount)
        )
        .scalar()
        or 0
    )
    @staticmethod
    def get_total_refunds(
       db: Session
):
      return (
        db.query(Payment)
        .filter(
            Payment.refund_amount > 0
        )
        .count()
    )