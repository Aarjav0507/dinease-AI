from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.restaurant_table import (
    RestaurantTableCreate,
    RestaurantTableResponse
)

from app.services.restaurant_table_service import (
    RestaurantTableService
)

router = APIRouter(
    prefix="/tables",
    tags=["Restaurant Tables"]
)


@router.post(
    "/",
    response_model=RestaurantTableResponse
)
def create_table(
    table_data: RestaurantTableCreate,
    db: Session = Depends(get_db)
):
    return RestaurantTableService.create_table(
        db,
        table_data
    )


@router.get(
    "/",
    response_model=List[RestaurantTableResponse]
)
def get_all_tables(
    db: Session = Depends(get_db)
):
    return RestaurantTableService.get_all_tables(
        db
    )


@router.get(
    "/{table_id}",
    response_model=RestaurantTableResponse
)
def get_table_by_id(
    table_id: int,
    db: Session = Depends(get_db)
):
    return RestaurantTableService.get_table_by_id(
        db,
        table_id
    )


@router.delete(
    "/{table_id}"
)
def delete_table(
    table_id: int,
    db: Session = Depends(get_db)
):
    return RestaurantTableService.delete_table(
        db,
        table_id
    )