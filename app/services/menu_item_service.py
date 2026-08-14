from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.schemas.menu_item import (
    MenuItemCreate,
    MenuItemUpdate
)

from app.repositories.menu_item_repository import (
    MenuItemRepository
)

from app.repositories.category_repository import (
    CategoryRepository
)


class MenuItemService:

    @staticmethod
    def create_menu_item(
        db: Session,
        menu_item_data: MenuItemCreate
    ) -> MenuItem:

        # Check category exists
        category = CategoryRepository.get_by_id(
            db,
            menu_item_data.category_id
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

        # Check duplicate item name
        existing_item = MenuItemRepository.get_by_name(
            db,
            menu_item_data.name
        )

        if existing_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Menu item already exists."
            )

        menu_item = MenuItem(
            category_id=menu_item_data.category_id,
            name=menu_item_data.name,
            description=menu_item_data.description,
            price=menu_item_data.price,
            image_url=menu_item_data.image_url,
            preparation_time=menu_item_data.preparation_time,
            calories=menu_item_data.calories,
            spice_level=menu_item_data.spice_level,
            is_veg=menu_item_data.is_veg
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

        menu_item = MenuItemRepository.get_by_id(
            db,
            menu_item_id
        )

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        return menu_item

    @staticmethod
    def update_menu_item(
        db: Session,
        menu_item_id: int,
        menu_item_data: MenuItemUpdate
    ):

        menu_item = MenuItemRepository.get_by_id(
            db,
            menu_item_id
        )

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        update_data = menu_item_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(
                menu_item,
                key,
                value
            )

        return MenuItemRepository.update(
            db,
            menu_item
        )

    @staticmethod
    def delete_menu_item(
        db: Session,
        menu_item_id: int
    ):

        menu_item = MenuItemRepository.get_by_id(
            db,
            menu_item_id
        )

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        MenuItemRepository.delete(
            db,
            menu_item
        )

        return {
            "message": "Menu item deleted successfully."
        }

    @staticmethod
    def get_menu_items_by_category(
        db: Session,
        category_id: int
    ):

        category = CategoryRepository.get_by_id(
            db,
            category_id
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

        return MenuItemRepository.get_by_category(
            db,
            category_id
        )