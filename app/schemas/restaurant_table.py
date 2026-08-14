from datetime import datetime

from pydantic import BaseModel,Field


class RestaurantTableCreate(BaseModel):
    table_number: str
    capacity: int = Field(gt=0)


class RestaurantTableResponse(BaseModel):
    id: int
    table_number: str
    capacity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True