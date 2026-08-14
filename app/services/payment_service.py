from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.payment import Payment

from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository

from app.core.razorpay_client import razorpay_client
from app.core.constants import (
    PAYMENT_PAID,
    CONFIRMED
)

class PaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        order_id: int,
        current_user
    ):

        # Get Order
        order = OrderRepository.get_by_id(
            db,
            order_id
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        # Ownership Check
        if order.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized"
            )

        # Existing Payment Check
        existing_payment = (
            PaymentRepository.get_by_order_id(
                db,
                order.id
            )
        )

        if existing_payment:
            return existing_payment

        # Reservation
        reservation = order.reservation

        if reservation.status != "PENDING_PAYMENT":
            raise HTTPException(
                status_code=400,
                detail="Reservation is not awaiting payment"
            )

        # Expiry Check (15 Minutes)
        expiry_time = (
            reservation.created_at +
            timedelta(minutes=15)
        )

        if datetime.utcnow() > expiry_time:

            reservation.status = "EXPIRED"

            order.order_status = "CANCELLED"

            order.payment_status = "FAILED"

            db.commit()

            raise HTTPException(
                status_code=400,
                detail="Reservation expired. Please create a new reservation."
            )

        # Convert Rupees -> Paise
        amount_in_paise = int(
            Decimal(str(order.total_amount)) * 100
        )

        # Create Razorpay Order
        razorpay_order = razorpay_client.order.create(
            {
                "amount": amount_in_paise,
                "currency": "INR"
            }
        )

        # Create Payment Record
        payment = Payment(
            order_id=order.id,
            razorpay_order_id=razorpay_order["id"],
            amount=order.total_amount,
            payment_status="PENDING",
            refund_amount=Decimal("0.00"),
            refund_status="NOT_APPLICABLE"
        )

        payment = PaymentRepository.create(
            db,
            payment
        )

        return payment

    @staticmethod
    def verify_payment(
        db: Session,
        payment_data,
        current_user
    ):

        # Get Payment
        payment = (
            PaymentRepository.get_by_razorpay_order_id(
                db,
                payment_data.razorpay_order_id
            )
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        order = payment.order

        # Ownership Check
        if order.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized"
            )

        # Already Verified
        if payment.payment_status ==  PAYMENT_PAID:
            return payment

        # Verify Razorpay Signature
        try:

            razorpay_client.utility.verify_payment_signature(
                {
                    "razorpay_order_id":
                        payment_data.razorpay_order_id,

                    "razorpay_payment_id":
                        payment_data.razorpay_payment_id,

                    "razorpay_signature":
                        payment_data.razorpay_signature
                }
            )

        except Exception:

            payment.payment_status = "FAILED"

            PaymentRepository.update(
                db,
                payment
            )

            raise HTTPException(
                status_code=400,
                detail="Payment verification failed"
            )

        # Update Payment
        payment.razorpay_payment_id = (
            payment_data.razorpay_payment_id
        )

        payment.razorpay_signature = (
            payment_data.razorpay_signature
        )

        payment.payment_status = "SUCCESS"

        # Update Order
        order.payment_status =  PAYMENT_PAID

        order.order_status = "CONFIRMED"

        # Update Reservation
        reservation = order.reservation

        reservation.status = CONFIRMED

        db.commit()

        db.refresh(payment)

        return payment
    @staticmethod
    def get_payment_by_id(
    db: Session,
    payment_id: int,
    current_user
):

     payment = PaymentRepository.get_by_id(
        db,
        payment_id
    )

     if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

     if payment.order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

     return payment