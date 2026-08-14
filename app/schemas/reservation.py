from datetime import date, time, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    table_id: int
    reservation_date: date
    start_time: time
    end_time: time
    guests_count: int = Field(gt=0)


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    table_id: int

    reservation_date: date
    start_time: time
    end_time: time

    guests_count: int

    reservation_charge: Decimal
    reservation_credit_remaining: Decimal

    status: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True