from fastapi import (
    APIRouter,
    Depends,
    status
)
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.menu_item import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse
)

from app.services.menu_item_service import (
    MenuItemService
)
from app.dependencies.admin import (
    get_current_admin
)
router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)


@router.post(
    "/",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_menu_item(
    menu_item: MenuItemCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return MenuItemService.create_menu_item(
        db,
        menu_item
    )


@router.get(
    "/",
    response_model=list[MenuItemResponse]
)
def get_all_menu_items(
    db: Session = Depends(get_db)
):
    return MenuItemService.get_all_menu_items(db)


@router.get(
    "/{menu_item_id}",
    response_model=MenuItemResponse
)
def get_menu_item_by_id(
    menu_item_id: int,
    db: Session = Depends(get_db)
):
    return MenuItemService.get_menu_item_by_id(
        db,
        menu_item_id
    )


@router.put(
    "/{menu_item_id}",
    response_model=MenuItemResponse
)
def update_menu_item(
    menu_item_id: int,
    menu_item: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return MenuItemService.update_menu_item(
        db,
        menu_item_id,
        menu_item
    )


@router.delete(
    "/{menu_item_id}"
)
def delete_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return MenuItemService.delete_menu_item(
        db,
        menu_item_id
    )


@router.get(
    "/category/{category_id}",
    response_model=list[MenuItemResponse]
)
def get_menu_items_by_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    return MenuItemService.get_menu_items_by_category(
        db,
        category_id
    )