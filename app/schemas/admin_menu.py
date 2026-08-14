from decimal import Decimal
from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    category_id: int
    name: str
    description: str
    price: Decimal
    image_url: str | None = None
    preparation_time: int
    calories: int
    spice_level: int
    is_veg: bool


class MenuItemUpdate(BaseModel):
    category_id: int
    name: str
    description: str
    price: Decimal
    image_url: str | None = None
    preparation_time: int
    calories: int
    spice_level: int
    is_veg: bool


class MenuAvailabilityUpdate(BaseModel):
    is_available: bool