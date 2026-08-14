from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.admin import (
    admin_required
)

from app.services.admin_service import (
    AdminService
)

from app.schemas.admin import (
    OrderStatusUpdate
)
from app.schemas.admin_table import (
    TableCreate,
    TableUpdate,
    TableAvailabilityUpdate
)
from app.schemas.admin_menu import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuAvailabilityUpdate
)
from app.schemas.system_settings import (
    SystemSettingsUpdate
)
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/orders")
def get_all_orders(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_all_orders(db)
    )


@router.get("/orders/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_order_by_id(
            db,
            order_id
        )
    )


@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.update_order_status(
            db,
            order_id,
            data.order_status
        )
    )
@router.get("/reservations")
def get_all_reservations(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_all_reservations(
            db
        )
    )
@router.get("/reservations/{reservation_id}")
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_reservation_by_id(
            db,
            reservation_id
        )
    )
@router.patch(
    "/reservations/{reservation_id}/confirm"
)
def confirm_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.confirm_reservation(
            db,
            reservation_id
        )
    )
@router.patch(
    "/reservations/{reservation_id}/cancel"
)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.cancel_reservation(
            db,
            reservation_id
        )
    )
@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_dashboard(
            db
        )
    )
@router.get("/revenue")
def get_revenue(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_revenue_analytics(
            db
        )
    )
@router.post("/tables")
def create_table(
    table_data: TableCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.create_table(
            db,
            table_data
        )
    )
@router.get("/tables")
def get_all_tables(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_all_tables(
            db
        )
    )
@router.get("/tables/{table_id}")
def get_table(
    table_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_table_by_id(
            db,
            table_id
        )
    )
@router.put("/tables/{table_id}")
def update_table(
    table_id: int,
    table_data: TableUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.update_table(
            db,
            table_id,
            table_data
        )
    )
@router.delete("/tables/{table_id}")
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.delete_table(
            db,
            table_id
        )
    )
@router.patch(
    "/tables/{table_id}/availability"
)
def update_availability(
    table_id: int,
    data: TableAvailabilityUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.update_table_availability(
            db,
            table_id,
            data.is_active
        )
    )
@router.post("/menu")
def create_menu_item(
    menu_data: MenuItemCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AdminService.create_menu_item(
        db,
        menu_data
    )
@router.get("/menu")
def get_all_menu_items(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AdminService.get_all_menu_items(db)
@router.get("/menu/{menu_item_id}")
def get_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AdminService.get_menu_item_by_id(
        db,
        menu_item_id
    )
@router.put("/menu/{menu_item_id}")
def update_menu_item(
    menu_item_id: int,
    menu_data: MenuItemUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AdminService.update_menu_item(
        db,
        menu_item_id,
        menu_data
    )
@router.delete("/menu/{menu_item_id}")
def delete_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AdminService.delete_menu_item(
        db,
        menu_item_id
    )
@router.patch("/menu/{menu_item_id}/availability")
def update_menu_availability(
    menu_item_id: int,
    data: MenuAvailabilityUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AdminService.update_menu_availability(
        db,
        menu_item_id,
        data.is_available
    )
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_all_users(
            db
        )
    )
@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_user_by_id(
            db,
            user_id
        )
    )
@router.patch("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.activate_user(
            db,
            user_id
        )
    )
@router.patch("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.deactivate_user(
            db,
            user_id
        )
    )
@router.patch("/users/{user_id}/make-admin")
def make_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.make_admin(
            db,
            user_id
        )
    )
@router.patch("/users/{user_id}/remove-admin")
def remove_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.remove_admin(
            db,
            user_id
        )
    )
@router.get("/settings")
def get_settings(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.get_system_settings(
            db
        )
    )
@router.patch("/settings")
def update_settings(
    data: SystemSettingsUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):

    return (
        AdminService.update_system_settings(
            db,
            data
        )
    )