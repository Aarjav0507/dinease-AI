from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.restaurant_table import RestaurantTable
from app.repositories.restaurant_table_repository import (
    RestaurantTableRepository
)
from app.schemas.restaurant_table import (
    RestaurantTableCreate
)


class RestaurantTableService:

    @staticmethod
    def create_table(
        db: Session,
        table_data: RestaurantTableCreate
    ):

        # Check duplicate table number
        existing_table = (
            RestaurantTableRepository
            .get_by_table_number(
                db,
                table_data.table_number
            )
        )

        if existing_table:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Table number already exists."
            )

        # Validate capacity
        if table_data.capacity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Capacity must be greater than 0."
            )

        table = RestaurantTable(
            table_number=table_data.table_number,
            capacity=table_data.capacity
        )

        return RestaurantTableRepository.create(
            db,
            table
        )

    @staticmethod
    def get_all_tables(
        db: Session
    ):
        return RestaurantTableRepository.get_all(db)

    @staticmethod
    def get_table_by_id(
        db: Session,
        table_id: int
    ):

        table = (
            RestaurantTableRepository
            .get_by_id(
                db,
                table_id
            )
        )

        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found."
            )

        return table

    @staticmethod
    def delete_table(
        db: Session,
        table_id: int
    ):

        table = (
            RestaurantTableRepository
            .get_by_id(
                db,
                table_id
            )
        )

        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found."
            )

        RestaurantTableRepository.delete(
            db,
            table
        )

        return {
            "message": "Table deleted successfully."
        }