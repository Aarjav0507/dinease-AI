from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem

from app.repositories.order_repository import OrderRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.reservation_repository import ReservationRepository
from app.services.system_settings_service import (
    SystemSettingsService
)


class OrderService:

    @staticmethod
    def create_order_from_reservation(
        db: Session,
        reservation_id: int,
        current_user
    ):
        settings = (
    SystemSettingsService.get_settings(
        db
    )
)

        # Get Reservation
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

        # Ownership Check
        if reservation.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to access this reservation"
            )

        # Status Check
        if reservation.status != "PENDING_PAYMENT":
            raise HTTPException(
                status_code=400,
                detail="Order can only be created for pending payment reservations"
            )

        # Prevent Duplicate Orders
        existing_order = (
            OrderRepository.get_by_reservation_id(
                db,
                reservation_id
            )
        )

        if existing_order:
            raise HTTPException(
                status_code=400,
                detail="Order already exists for this reservation"
            )

        # Get User Cart
        cart = (
            CartRepository.get_by_user_id(
                db,
                current_user.id
            )
        )

        if not cart:
            raise HTTPException(
                status_code=400,
                detail="Cart not found"
            )

        # Get Cart Items
        cart_items = (
            CartRepository.get_cart_items(
                db,
                cart.id
            )
        )

        if not cart_items:
            raise HTTPException(
                status_code=400,
                detail="Cart is empty"
            )

        # Calculate Food Total
        food_total = Decimal("0.00")

        for cart_item in cart_items:

            item_total = (
                Decimal(str(cart_item.menu_item.price))
                * cart_item.quantity
            )

            food_total += item_total

        # Reservation Fee Logic
        reservation_charge = Decimal("0.00")

        if food_total >= Decimal("1000.00"):

            reservation_charge = Decimal("0.00")

            reservation.reservation_fee_waived = True

            reservation.reservation_credit_remaining = Decimal("0.00")

        else:

            reservation_charge = Decimal(
                str(reservation.reservation_charge)
            )

            reservation.reservation_fee_waived = False

        total_amount = (
            food_total +
            reservation_charge
        )

        # Create Order
        order = Order(
            reservation_id=reservation.id,
            user_id=current_user.id,

            food_total_amount=food_total,

            subtotal_amount=food_total,

            reservation_charge=reservation_charge,

            reservation_credit_used=Decimal("0.00"),

            total_amount=total_amount,

            payment_status="PENDING",

            order_status="PENDING"
        )

        db.add(order)

        # Generate order.id
        db.flush()

        # Create Order Items
        for cart_item in cart_items:

            order_item = OrderItem(
                order_id=order.id,

                menu_item_id=cart_item.menu_item_id,

                quantity=cart_item.quantity,

                price_at_order_time=cart_item.menu_item.price
            )

            db.add(order_item)
                   
        CartRepository.clear_cart(
                   db,
                   cart.id
            )
            
            
       

        db.commit()

        db.refresh(order)

        return order

    @staticmethod
    def get_order_by_id(
        db: Session,
        order_id: int,
        current_user
    ):

        order = (
            OrderRepository.get_by_id(
                db,
                order_id
            )
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized"
            )

        return order

    @staticmethod
    def get_my_orders(
        db: Session,
        current_user
    ):

        return (
            OrderRepository.get_user_orders(
                db,
                current_user.id
            )
        )