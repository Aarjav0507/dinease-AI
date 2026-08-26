from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.order_repository import (
    OrderRepository
)

from app.core.constants import (
    ORDER_PENDING,
    ORDER_CONFIRMED,
    ORDER_PREPARING,
    ORDER_READY,
    ORDER_SERVED,
    ORDER_COMPLETED
)
from app.repositories.reservation_repository import (
    ReservationRepository
)

from app.repositories.payment_repository import (
    PaymentRepository
)

from app.core.constants import (
    CONFIRMED,
    CANCELLED,
    ORDER_CANCELLED,
    PAYMENT_PAID,
    REFUND_COMPLETED,
    REFUND_PERCENTAGE
)

from decimal import Decimal

from app.core.razorpay_client import razorpay_client
from app.repositories.user_repository import UserRepository
from app.models.restaurant_table import RestaurantTable

from app.repositories.restaurant_table_repository import (
    RestaurantTableRepository
)

from app.schemas.admin_table import (
    TableCreate,
    TableUpdate
)
from app.models.menu_item import MenuItem

from app.repositories.menu_item_repository import (
    MenuItemRepository
)

from app.schemas.admin_menu import (
    MenuItemCreate,
    MenuItemUpdate
)
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.system_setting import SystemSettings

from app.repositories.system_setting_repository import (
    SystemSettingsRepository
)

from app.schemas.system_settings import (
    SystemSettingsUpdate
)

class AdminService:

    @staticmethod
    def get_all_orders(
        db: Session
    ):
        return (
            OrderRepository.get_all_orders(db)
        )

    @staticmethod
    def get_order_by_id(
        db: Session,
        order_id: int
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

        return order

    @staticmethod
    def update_order_status(
        db: Session,
        order_id: int,
        new_status: str
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

        valid_statuses = [
            ORDER_PENDING,
            ORDER_CONFIRMED,
            ORDER_PREPARING,
            ORDER_READY,
            ORDER_SERVED,
            ORDER_COMPLETED
        ]

        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail="Invalid order status"
            )

        order.order_status = new_status

        return (
            OrderRepository.update_order(
                db,
                order
            )
        )
    @staticmethod
    def get_all_reservations(
      db: Session
):
      return (
        ReservationRepository.get_all(db)
    )
    @staticmethod
    def get_reservation_by_id(
       db: Session,
       reservation_id: int
):

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

       return reservation

    @staticmethod
    def confirm_reservation(
        db: Session,
        reservation_id: int
):

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

        reservation.status = CONFIRMED

        return (
        ReservationRepository.update(
            db,
            reservation
        )
    )
    @staticmethod
    def cancel_reservation(
       db: Session,
       reservation_id: int
):

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

       if payment.payment_status == PAYMENT_PAID:

        refund_amount = (
            Decimal(str(payment.amount))
            * Decimal(str(REFUND_PERCENTAGE))
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

       return {
        "message": "Reservation cancelled successfully"
    }
    @staticmethod
    def get_dashboard(
       db: Session
):

      return {
        "total_users":
            UserRepository.count_users(db),

        "total_reservations":
            ReservationRepository.count_reservations(db),

        "total_orders":
            OrderRepository.count_orders(db),

        "total_payments":
            PaymentRepository.count_payments(db),

        "total_revenue":
            float(
                PaymentRepository.total_revenue(db)
            )
    }
    @staticmethod
    def get_revenue_analytics(
      db: Session
):

      gross_revenue = float(
        PaymentRepository.get_gross_revenue(
            db
        )
    )

      refund_amount = float(
        PaymentRepository.get_total_refund_amount(
            db
        )
    )

      total_refunds = (
        PaymentRepository.get_total_refunds(
            db
        )
    )

      net_revenue = (
        gross_revenue -
        refund_amount
    )

      return {
        "gross_revenue": gross_revenue,
        "refund_amount": refund_amount,
        "net_revenue": net_revenue,
        "total_refunds": total_refunds
    }
    @staticmethod
    def create_table(
       db: Session,
       table_data: TableCreate
):

      existing_table = (
        RestaurantTableRepository
        .get_by_table_number(
            db,
            table_data.table_number
        )
    )

      if existing_table:
        raise HTTPException(
            status_code=400,
            detail="Table number already exists"
        )

      table = RestaurantTable(
        table_number=table_data.table_number,
        capacity=table_data.capacity,
        is_active=True
    )

      return (
        RestaurantTableRepository.create(
            db,
            table
        )
    )
    @staticmethod
    def get_all_tables(
      db: Session
):
      return (
        RestaurantTableRepository.get_all(
            db
        )
    )
    @staticmethod
    def get_table_by_id(
      db: Session,
      table_id: int
):

      table = (
        RestaurantTableRepository.get_by_id(
            db,
            table_id
        )
    )

      if not table:
        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

      return table
    @staticmethod
    def update_table(
      db: Session,
      table_id: int,
      table_data: TableUpdate
):

      table = (
        RestaurantTableRepository.get_by_id(
            db,
            table_id
        )
    )

      if not table:
        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

      table.table_number = (
        table_data.table_number
    )

      table.capacity = (
        table_data.capacity
    )

      return (
        RestaurantTableRepository.update(
            db,
            table
        )
    )
    @staticmethod
    def delete_table(
       db: Session,
       table_id: int
):

       table = (
        RestaurantTableRepository.get_by_id(
            db,
            table_id
        )
    )

       if not table:
          raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

       RestaurantTableRepository.delete(
        db,
        table
    )

       return {
        "message": "Table deleted successfully"
    }
    @staticmethod
    def update_table_availability(
      db: Session,
      table_id: int,
      is_active: bool
):

      table = (
        RestaurantTableRepository.get_by_id(
            db,
            table_id
        )
    )

      if not table:
        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

      table.is_active = is_active

      return (
        RestaurantTableRepository.update(
            db,
            table
        )
    )
    @staticmethod
    def create_menu_item(
      db: Session,
      menu_data: MenuItemCreate
):

      existing_item = (
        MenuItemRepository.get_by_name(
            db,
            menu_data.name
        )
    )

      if existing_item:
        raise HTTPException(
            status_code=400,
            detail="Menu item already exists"
        )

      menu_item = MenuItem(
        category_id=menu_data.category_id,
        name=menu_data.name,
        description=menu_data.description,
        price=menu_data.price,
        image_url=menu_data.image_url,
        preparation_time=menu_data.preparation_time,
        calories=menu_data.calories,
        spice_level=menu_data.spice_level,
        is_veg=menu_data.is_veg,
        is_available=True
    )

      return MenuItemRepository.create(
        db,
        menu_item
    )
    @staticmethod
    def get_all_menu_items(
     db: Session
):
     return MenuItemRepository.get_all(db)
    @staticmethod
    def get_menu_item_by_id(
      db: Session,
      menu_item_id: int
):

      menu_item = (
        MenuItemRepository.get_by_id(
            db,
            menu_item_id
        )
    )

      if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

      return menu_item
    @staticmethod
    def update_menu_item(
      db: Session,
      menu_item_id: int,
      menu_data: MenuItemUpdate
):

      menu_item = (
        MenuItemRepository.get_by_id(
            db,
            menu_item_id
        )
    )

      if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

      menu_item.category_id = menu_data.category_id
      menu_item.name = menu_data.name
      menu_item.description = menu_data.description
      menu_item.price = menu_data.price
      menu_item.image_url = menu_data.image_url
      menu_item.preparation_time = menu_data.preparation_time
      menu_item.calories = menu_data.calories
      menu_item.spice_level = menu_data.spice_level
      menu_item.is_veg = menu_data.is_veg

      return MenuItemRepository.update(
        db,
        menu_item
    )
    @staticmethod
    def delete_menu_item(
      db: Session,
      menu_item_id: int
):

      menu_item = (
        MenuItemRepository.get_by_id(
            db,
            menu_item_id
        )
    )

      if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

      MenuItemRepository.delete(
        db,
        menu_item
    )

      return {
        "message": "Menu item deleted successfully"
    }
    @staticmethod
    def update_menu_availability(
      db: Session,
      menu_item_id: int,
      is_available: bool
):

      menu_item = (
        MenuItemRepository.get_by_id(
            db,
            menu_item_id
        )
    )

      if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

      menu_item.is_available = is_available

      return MenuItemRepository.update(
        db,
        menu_item
    )
    @staticmethod
    def get_all_users(
      db: Session
):
      return UserRepository.get_all(db)
    @staticmethod
    def get_user_by_id(
      db: Session,
      user_id: int
):

      user = (
        UserRepository.get_by_id(
            db,
            user_id
        )
    )

      if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

      return user
    @staticmethod
    def activate_user(
      db: Session,
      user_id: int
):

      user = (
        UserRepository.get_by_id(
            db,
            user_id
        )
    )

      if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

      user.is_active = True

      return (
        UserRepository.update(
            db,
            user
        )
    )
    @staticmethod
    def deactivate_user(
      db: Session,
      user_id: int
):

      user = (
        UserRepository.get_by_id(
            db,
            user_id
        )
    )

      if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

      user.is_active = False

      return (
        UserRepository.update(
            db,
            user
        )
    )
    @staticmethod
    def make_admin(
      db: Session,
      user_id: int
):

      user = (
        UserRepository.get_by_id(
            db,
            user_id
        )
    )

      if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

      user.role = "ADMIN"

      return (
        UserRepository.update(
            db,
            user
        )
    )
    @staticmethod
    def remove_admin(
      db: Session,
      user_id: int
):

      user = (
        UserRepository.get_by_id(
            db,
            user_id
        )
    )

      if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

      if user.role != "ADMIN":
        raise HTTPException(
            status_code=400,
            detail="User is not an admin"
        )

      admin_count = (
        UserRepository.count_admins(
            db
        )
    )

      if admin_count <= 1:
        raise HTTPException(
            status_code=400,
            detail="Cannot remove last admin"
        )

      user.role = "customer"

      return (
        UserRepository.update(
            db,
            user
        )
    )
    @staticmethod
    def get_system_settings(
      db: Session
):

     settings = (
        SystemSettingsRepository.get_settings(
            db
        )
    )

     if not settings:

        settings = SystemSettings()

        settings = (
            SystemSettingsRepository.create(
                db,
                settings
            )
        )

     return settings
    @staticmethod
    def update_system_settings(
      db: Session,
      data: SystemSettingsUpdate
):

      settings = (
        SystemSettingsRepository.get_settings(
            db
        )
    )

      if not settings:

        settings = SystemSettings()

        settings = (
            SystemSettingsRepository.create(
                db,
                settings
            )
        )

      update_data = data.model_dump(
        exclude_unset=True
    )

      for key, value in update_data.items():

        setattr(
            settings,
            key,
            value
        )

      return (
        SystemSettingsRepository.update(
            db,
            settings
        )
    )