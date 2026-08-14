from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field


# -----------------------------
# Create Menu Item
# -----------------------------
class MenuItemCreate(BaseModel):
    category_id: int

    name: str = Field(
        ...,
        min_length=3,
        max_length=150
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=500
    )

    price: Decimal

    image_url: str | None = None

    preparation_time: int = Field(
        ...,
        gt=0
    )

    calories: int = Field(
        ...,
        gt=0
    )

    spice_level: int = Field(
        default=1,
        ge=1,
        le=5
    )

    is_veg: bool


# -----------------------------
# Update Menu Item
# -----------------------------
class MenuItemUpdate(BaseModel):

    category_id: int | None = None

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=150
    )

    description: str | None = Field(
        default=None,
        min_length=5,
        max_length=500
    )

    price: Decimal | None = None

    image_url: str | None = None

    preparation_time: int | None = Field(
        default=None,
        gt=0
    )

    calories: int | None = Field(
        default=None,
        gt=0
    )

    spice_level: int | None = Field(
        default=None,
        ge=1,
        le=5
    )

    is_veg: bool | None = None

    is_available: bool | None = None


# -----------------------------
# Response Schema
# -----------------------------
class MenuItemResponse(BaseModel):

    id: int
    category_id: int

    name: str
    description: str

    price: Decimal

    image_url: str | None

    preparation_time: int
    calories: int
    spice_level: int

    rating: Decimal

    is_veg: bool
    is_available: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True