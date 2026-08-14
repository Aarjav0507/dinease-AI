from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate
)
from app.repositories.category_repository import (
    CategoryRepository
)


class CategoryService:

    @staticmethod
    def create_category(
        db: Session,
        category_data: CategoryCreate
    ) -> Category:

        # Check duplicate name
        existing_category = (
            CategoryRepository.get_by_name(
                db,
                category_data.name
            )
        )

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists."
            )

        category = Category(
            name=category_data.name,
            description=category_data.description,
            image_url=category_data.image_url
        )

        return CategoryRepository.create(
            db,
            category
        )

    @staticmethod
    def get_all_categories(
        db: Session
    ):
        return CategoryRepository.get_all(db)

    @staticmethod
    def get_category_by_id(
        db: Session,
        category_id: int
    ):

        category = (
            CategoryRepository.get_by_id(
                db,
                category_id
            )
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

        return category

    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        category_data: CategoryUpdate
    ):

        category = (
            CategoryRepository.get_by_id(
                db,
                category_id
            )
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

        update_data = (
            category_data.model_dump(
                exclude_unset=True
            )
        )

        for key, value in update_data.items():
            setattr(
                category,
                key,
                value
            )

        return CategoryRepository.update(
            db,
            category
        )

    @staticmethod
    def delete_category(
        db: Session,
        category_id: int
    ):

        category = (
            CategoryRepository.get_by_id(
                db,
                category_id
            )
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

        CategoryRepository.delete(
            db,
            category
        )

        return {
            "message":
            "Category deleted successfully."
        }