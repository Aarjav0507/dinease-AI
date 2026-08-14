from datetime import datetime, date, time

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.reservation import Reservation
from app.models.restaurant_table import RestaurantTable

from app.repositories.reservation_repository import (
    ReservationRepository
)

from app.repositories.restaurant_table_repository import (
    RestaurantTableRepository
)

from app.schemas.reservation import (
    ReservationCreate
)
from app.core.constants import (
    RESERVATION_CHARGE_PER_HOUR_PER_GUEST
)
from datetime import timedelta
from decimal import Decimal

from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository

from app.core.razorpay_client import razorpay_client

from app.core.constants import (
    CONFIRMED,
    CANCELLED,
    ORDER_CANCELLED,
    PAYMENT_PAID,
    REFUND_COMPLETED,
   
)
from app.services.system_settings_service import (
    SystemSettingsService
)


class ReservationService:

    @staticmethod
    
    def calculate_reservation_charge(
        db: Session,
        guests_count,
        start_time,
        end_time
) -> float:

        start_dt = datetime.combine(
            date.today(),
            start_time
        )

        end_dt = datetime.combine(
            date.today(),
            end_time
        )

        duration_hours = (
            end_dt - start_dt
        ).total_seconds() / 3600

        if duration_hours <= 1:
            return 0

        extra_hours = duration_hours - 1
        settings = (
          SystemSettingsService.get_settings(
           db
    )
)

       

        return (
               extra_hours
                     * settings.reservation_charge_per_hour_per_guest
                      * guests_count
)

    @staticmethod
    def create_reservation(
        db: Session,
        user_id: int,
        reservation_data: ReservationCreate
    ):

        # Validate time range
        if reservation_data.end_time <= reservation_data.start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be greater than start time."
            )

        # Get table
        table = RestaurantTableRepository.get_by_id(
            db,
            reservation_data.table_id
        )

        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found."
            )

        # Capacity validation
        if reservation_data.guests_count > table.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Table capacity is only {table.capacity}."
            )

        # Check overlapping reservation
        existing_reservation = (
            ReservationRepository
            .get_overlapping_reservation(
                db=db,
                table_id=reservation_data.table_id,
                reservation_date=reservation_data.reservation_date,
                start_time=reservation_data.start_time,
                end_time=reservation_data.end_time
            )
        )

        if existing_reservation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Table is already reserved for this slot."
            )

        reservation_charge = (
            ReservationService
            .calculate_reservation_charge(db,
                reservation_data.guests_count,
                reservation_data.start_time,
                reservation_data.end_time
            )
        )

        reservation = Reservation(
            user_id=user_id,
            table_id=reservation_data.table_id,
            reservation_date=reservation_data.reservation_date,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time,
            guests_count=reservation_data.guests_count,
            reservation_charge=reservation_charge,
            reservation_credit_remaining=reservation_charge,
            status="PENDING_PAYMENT"
        )

        return ReservationRepository.create(
            db,
            reservation
        )

    @staticmethod
    def get_all_reservations(
        db: Session
    ):
        return ReservationRepository.get_all(db)

    @staticmethod
    def get_user_reservations(
        db: Session,
        user_id: int
    ):
        return ReservationRepository.get_user_reservations(
            db,
            user_id
        )

    @staticmethod
    def get_reservation_by_id(
        db: Session,
        reservation_id: int
    ):

        reservation = (
            ReservationRepository
            .get_by_id(
                db,
                reservation_id
            )
        )

        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservation not found."
            )

        return reservation
    @staticmethod
    def cancel_reservation(
        
    db: Session,
    reservation_id: int,
    current_user
):
       settings = (
    SystemSettingsService.get_settings(
        db
    )
)

       reservation = (
         ReservationRepository.get_by_id(
            db,
            reservation_id
        )
    )

       if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

       if reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

       if reservation.status != CONFIRMED:
        raise HTTPException(
            status_code=400,
            detail="Only confirmed reservations can be cancelled"
        )

       reservation_datetime = datetime.combine(
        reservation.reservation_date,
        reservation.start_time
    )

       cancellation_deadline = (
        reservation_datetime
        - timedelta(
                      hours=settings.cancellation_window_hours
)
    )

       if datetime.utcnow() > cancellation_deadline:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Reservation can only be cancelled "
                f"{settings.cancellation_window_hours} hour(s) before start time"
            )
        )

       order = reservation.order

       if not order:
        raise HTTPException(
            status_code=400,
            detail="Order not found"
        )

       payment = (
        PaymentRepository.get_by_order_id(
            db,
            order.id
        )
    )

       if not payment:
        raise HTTPException(
            status_code=400,
            detail="Payment not found"
        )

       if payment.payment_status != PAYMENT_PAID:
        raise HTTPException(
            status_code=400,
            detail="Payment is not completed"
        )

       refund_amount = (
        Decimal(str(payment.amount))
        * Decimal(str(settings.refund_percentage))
        / Decimal("100")
    )

       refund_amount = refund_amount.quantize(
        Decimal("0.01")
    )

       refund_response = (
        razorpay_client.payment.refund(
            payment.razorpay_payment_id,
            {
                "amount": int(refund_amount * 100)
            }
        )
    )

       payment.refund_id = refund_response["id"]

       payment.refund_amount = refund_amount

       payment.refund_status = REFUND_COMPLETED

       reservation.status = CANCELLED

       order.order_status = ORDER_CANCELLED

       db.commit()

       db.refresh(payment)

       return {
        "message": "Reservation cancelled successfully",
        "refund_amount": float(refund_amount),
        "refund_id": refund_response["id"]
    }